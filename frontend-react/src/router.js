import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";

import HomePage from "./components/HomePage";
import AdminHome from "./components/AdminHome";
import ApplyForVisit from "./components/ApplyForVisit";
import LoginForm from "./components/LoginForm";
import RequestsList from "./components/RequestsList";
import SingleRequest from "./components/SingleRequest";
import UsersList from "./components/UsersList";
import SingleUser from "./components/SingleUser";
import {authStore} from "./store/auth";
import NavigationBar from "./components/NavigationBar";

function RouterView() {
    const PrivateRoute = ({children}) => {
        const hasPrivilegedAccess = authStore.hasPrivilegedAccess
        return hasPrivilegedAccess ? children : <Navigate to="/login"/>;
    };

    return (
        <BrowserRouter>
            <NavigationBar />
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/applyForVisit" element={<ApplyForVisit/>}/>
                <Route path="/login" element={<LoginForm/>}/>
                <Route
                    path="/home"
                    element={
                        <PrivateRoute>
                            <AdminHome/>
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/requests"
                    element={
                        <PrivateRoute>
                            <RequestsList/>
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/requests/:id"
                    element={
                        <PrivateRoute>
                            <SingleRequest/>
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/users"
                    element={
                        <PrivateRoute>
                            <UsersList/>
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/users/:id"
                    element={
                        <PrivateRoute>
                            <SingleUser/>
                        </PrivateRoute>
                    }
                />

            </Routes>
        </BrowserRouter>
    );
}

export default RouterView;
