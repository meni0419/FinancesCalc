import {BrowserRouter as Router, Navigate, Route, Routes, useNavigate,} from "react-router-dom";
import {MaterialReactTable} from "material-react-table";
import React, {useEffect, useState} from "react";
import {Alert, createTheme, CssBaseline, Snackbar, ThemeProvider} from "@mui/material"; // Import material components

const Login = () => {
    const [snackbar, setSnackbar] = useState({
        open: false,
        message: "",
        severity: "info", // "info", "success", "warning", "error"
    });

    const handleClose = () => {
        setSnackbar({...snackbar, open: false});
    };
    const handleSubmit = async (event) => {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;

        try {
            // Get CSRF token from cookies (or an endpoint)
            const csrfToken = document.cookie
                .split('; ')
                .find((row) => row.startsWith('csrftoken='))
                ?.split('=')[1];

            const response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken, // Send CSRF token
                },
                body: JSON.stringify({username, password}),
            });

            const result = await response.json();

            if (response.ok) {
                const {access, refresh} = result;
                localStorage.setItem("accessToken", access);
                localStorage.setItem("refreshToken", refresh);
                window.location.href = "/employees";
            } else {
                // Handle errors
                console.error("Login error:", result.error);
                setSnackbar({
                    open: true,
                    message: result.error || "Invalid login credentials",
                    severity: "error",
                });
            }
        } catch (err) {
            console.error("Fetch error:", err);
            setSnackbar({
                open: true,
                message: "Something went wrong. Please try again later.",
                severity: "error",
            });
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <h1>Login Page</h1>
                <form className="login-form" onSubmit={handleSubmit}>
                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" name="username" required/>
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" required/>
                    <button type="submit">Login</button>
                </form>
                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={handleClose}
                >
                    <Alert
                        onClose={handleClose}
                        severity={snackbar.severity}
                        sx={{width: '100%'}}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>
            </div>
        </div>
    );
};

const Employees = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [isDarkMode, setIsDarkMode] = useState(false); // Добавлено состояние для темы
    const [snackbar, setSnackbar] = useState({
        open: false,
        message: "",
        severity: "info", // "info", "success", "warning", "error"
    });
    const navigate = useNavigate(); // Добавлен хук useNavigate

    // Создание тем
    const lightTheme = createTheme({
        palette: {
            mode: "light",
        },
    });

    const darkTheme = createTheme({
        palette: {
            mode: "dark",
        },
    });

    // Функция для переключения темы
    const toggleTheme = () => {
        setIsDarkMode((prevTheme) => !prevTheme);
    };

    const handleLogout = () => {
        // Clear tokens on logout
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        window.location.href = "/login";
    };

    const fetchEmployees = async () => {
        try {
            const accessToken = localStorage.getItem("accessToken");

            if (!accessToken) {
                throw new Error("No access token found");
            }

            const response = await fetch("/api/employees/", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
            });

            if (!response.ok) {
                // Handling errors
                if (response.status === 401) {
                    console.error("Access token expired.");
                    const newAccessToken = await refreshAccessToken();
                    if (newAccessToken) {
                        fetchEmployees(); // Retry!
                    } else {
                        throw new Error("Could not refresh access token");
                    }
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            } else {
                const result = await response.json();
                setData(result);
            }
        } catch (error) {
            console.error("Failed to fetch employees:", error);
            setError(true);
            setSnackbar({
                open: true,
                message: "Unauthorized. Please log in again.",
                severity: "error",
            });
            navigate("/login");
        } finally {
            setLoading(false);
        }
    };

    const refreshAccessToken = async () => {
        try {
            const refreshToken = localStorage.getItem("refreshToken");

            if (!refreshToken) {
                throw new Error("No refresh token found");
            }

            const response = await fetch("/api/token/refresh/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({refresh: refreshToken}),
            });

            if (response.ok) {
                const {access} = await response.json();
                localStorage.setItem("accessToken", access); // Save new access token
                return access; // Return new token
            } else {
                throw new Error("Failed to refresh token");
            }
        } catch (err) {
            console.error("Error refreshing access token:", err);
            localStorage.removeItem("accessToken"); // Clear invalid tokens
            localStorage.removeItem("refreshToken");
            setSnackbar({
                open: true,
                message: "Token refresh failed. Redirecting to login.",
                severity: "error",
            });
            window.location.href = "/login";
            return null;
        }
    };

    useEffect(() => {
        const currentTheme = isDarkMode ? "dark" : "light";
        document.body.setAttribute("data-theme", currentTheme);
        fetchEmployees();
    }, [isDarkMode]);

    if (error) {
        navigate("/login");
        return null;
    }

    const columns = Object.keys(data[0] || {}).map((key) => ({
        accessorKey: key,
        header: key.replace(/_/g, " ").toUpperCase(),
    }));

    return (
        <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
            <CssBaseline/>
            <div style={{padding: "20px", backgroundColor: "var(--bg-color)", color: "var(--text-color)"}}>
                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "20px"
                }}>
                    <h1 style={{
                        backgroundColor: "var(--header-bg-color)",
                        color: "var(--header-text-color)",
                        padding: "10px",
                        borderRadius: "5px"
                    }}>
                        Employees
                    </h1>
                    <div>
                        <button
                            onClick={toggleTheme}
                            style={{
                                marginRight: "10px",
                                padding: "10px 20px",
                                backgroundColor: "var(--button-bg-color)",
                                color: "var(--button-text-color)",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer",
                            }}
                        >
                            Toggle Theme
                        </button>
                        <button
                            onClick={handleLogout}
                            style={{
                                padding: "10px 20px",
                                backgroundColor: "var(--button-bg-color)",
                                color: "var(--button-text-color)",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer",
                            }}
                        >
                            Logout
                        </button>
                    </div>
                </div>
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <MaterialReactTable
                        columns={columns}
                        data={data}
                        enableColumnOrdering={true}
                        enableColumnResizing={true}
                        enableHiding={true}
                        enableSorting={true}
                    />
                )}
                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={() => setSnackbar({...snackbar, open: false})}
                >
                    <Alert
                        onClose={() => setSnackbar({...snackbar, open: false})}
                        severity={snackbar.severity}
                        sx={{width: '100%'}}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>
            </div>
        </ThemeProvider>
    );
};

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(null); // Null during initial check

    const checkLoginStatus = async () => {
        const accessToken = localStorage.getItem("accessToken");

        // Token not found
        if (!accessToken) {
            console.log("No token found. User is not logged in.");
            setIsLoggedIn(false);
            return;
        }

        try {
            const response = await fetch("/api/employees/", {
                method: "GET",
                headers: {Authorization: `Bearer ${accessToken}`},
            });

            if (response.status === 401) {
                console.warn("Token invalid or expired. Logging out the user.");
                localStorage.removeItem("accessToken");
                setIsLoggedIn(false);
            } else if (response.ok) {
                console.log("Token valid. User is logged in.");
                setIsLoggedIn(true);
            }
        } catch (err) {
            console.error("Error validating token:", err);
            setIsLoggedIn(false);
        }
    };

    useEffect(() => {
        checkLoginStatus(); // Dynamically check login status on mount
    }, []);

    // Avoid rendering routes until login status is known
    if (isLoggedIn === null) {
        return <div>Loading...</div>;
    }

    return (
        <Router>
            <Routes>
                {/* Conditionally redirect based on login state */}
                <Route path="/" element={<Navigate to={isLoggedIn ? "/employees" : "/login"} replace/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route
                    path="/employees"
                    element={isLoggedIn ? <Employees/> : <Navigate to="/login" replace/>}
                />
                <Route path="*" element={<Navigate to="/" replace/>}/>
            </Routes>
        </Router>
    );
};

export default App;