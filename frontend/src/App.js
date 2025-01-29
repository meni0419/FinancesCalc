import {BrowserRouter as Router, Route, Routes, Navigate} from "react-router-dom";
import {MaterialReactTable} from "material-react-table";
import {useNavigate} from "react-router-dom";
import React, {useState, useEffect, createContext} from "react";
import {ThemeProvider, createTheme, CssBaseline} from "@mui/material";

const Login = () => {
    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent form reload
        const form = event.target;

        const username = form.username.value;
        const password = form.password.value;

        try {
            const response = await fetch("/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({username, password}),
            });

            if (response.redirected) {
                // Login successful, update state and redirect to /employees/
                window.location.href = response.url; // Redirect to employees list
            } else {
                const error = await response.text(); // Show error message
                console.error("Login failed:", error);
                alert("Failed to login: " + error);
            }
        } catch (err) {
            console.error("Login error:", err);
        }
    };

    return (
        <div style={{padding: "20px"}}>
            <h1>Login Page</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" name="username" required/>
                <br/>
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" name="password" required/>
                <br/>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

const Employees = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [isDarkMode, setIsDarkMode] = useState(false); // Theme toggle state
    const navigate = useNavigate();

    // Light and dark themes for MaterialReactTable
    const lightTheme = createTheme({
        palette: {
            mode: "light",
            background: {paper: "#ffffff"},
            text: {primary: "#000000"},
        },
        components: {
            MuiTable: {
                styleOverrides: {
                    root: {
                        border: "1px solid #cccccc",
                    },
                },
            },
        },
    });

    const darkTheme = createTheme({
        palette: {
            mode: "dark",
            background: {paper: "#121212"},
            text: {primary: "#ffffff"},
        },
        components: {
            MuiTable: {
                styleOverrides: {
                    root: {
                        border: "1px solid #444444",
                    },
                },
            },
        },
    });

    // Handle logout
    const handleLogout = async () => {
        try {
            const response = await fetch("/logout/", {method: "POST"});
            if (response.ok) {
                document.cookie = "access_token=; Max-Age=0; path=/;";
                document.cookie = "refresh_token=; Max-Age=0; path=/;";
                navigate("/login");
            } else {
                console.error("Failed to log out.");
            }
        } catch (err) {
            console.error("Logout error:", err);
        }
    };

    // Toggle theme
    const toggleTheme = () => {
        setIsDarkMode((prevTheme) => !prevTheme);
        document.body.classList.toggle("dark");
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const accessToken = document.cookie
                    .split("; ")
                    .find((row) => row.startsWith("access_token="))
                    ?.split("=")[1];

                if (!accessToken) {
                    throw new Error("No access token found");
                }

                const response = await fetch("/api/employees/", {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error("Failed to load employees:", error);
                setError(true);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

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
            </div>
        </ThemeProvider>
    );
};

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(null); // Null during initial check

    const checkLoginStatus = async () => {
        // Retrieve the token from cookies
        const accessToken = document.cookie
            .split("; ")
            .find((row) => row.startsWith("access_token="))?.split("=")[1];

        // If no token, user is not logged in
        if (!accessToken) {
            setIsLoggedIn(false);
            return;
        }

        try {
            // Optional: Validate token with API to ensure it's not expired or invalid
            const response = await fetch("/api/employees/", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            });

            if (response.status === 401) {
                // Token expired/invalid, log user out
                setIsLoggedIn(false);
                return;
            }

            // Token is valid
            setIsLoggedIn(true);
        } catch (err) {
            console.error("Token validation failed:", err);
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