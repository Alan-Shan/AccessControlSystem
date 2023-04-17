import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {authStore} from "../store/auth";


const LoginForm = () => {
    const history = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [validationFailed, setValidationFailed] = useState([]);

    useEffect(() => {
        if (authStore.user) {
            history("/home");
        }
    }, [history]);

    function validateFields() {
        setValidationFailed([]);
        let successful = true;
        if (!username) {
            setValidationFailed((prev) => [...prev, "username"]);
            successful = false;
        }
        if (!password) {
            setValidationFailed((prev) => [...prev, "password"]);
            successful = false;
        }

        return successful;
    }

    async function login() {
        if (!validateFields()) {
            return;
        }
        try {
            await authStore.login({username, password})
            history("/home");
        } catch (e) {
            setError("Неверное имя пользователя или пароль");
            console.debug(authStore.user);
        }
    }

    const handleKeyDown = async (event) => {
        if (event.key === "Enter") {
            await login();
        }
    }

    return (
        <div className={"container flex mt-4"}>
        <main className="form-signin">
            <form onKeyDown={handleKeyDown}>
                <h1 className="h3 mb-3 fw-normal">Авторизация</h1>
                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}
                <div className={`form-floating${validationFailed.includes("username") ? " is-invalid" : ""}`}>
                    <input
                        type="text"
                        className="form-control"
                        value={username}
                        id="usernameInput"
                        placeholder="user"
                        onChange={(event) => setUsername(event.target.value)}
                    />
                    <label htmlFor="usernameInput">Имя пользователя</label>
                    {validationFailed.includes("username") && (
                        <div className="invalid-feedback">Поле не может быть пустым</div>
                    )}
                </div>
                <div className={`form-floating${validationFailed.includes("password") ? " is-invalid" : ""}`}>
                    <input
                        type="password"
                        className="form-control"
                        value={password}
                        id="passwordInput"
                        placeholder="****"
                        onChange={(event) => setPassword(event.target.value)}
                    />
                    <label htmlFor="passwordInput">Пароль</label>
                    {validationFailed.includes("password") && (
                        <div className="invalid-feedback">Поле не может быть пустым</div>
                    )}
                </div>
                <div className="checkbox mb-3">
                    <label>
                        <input type="checkbox" value="remember-me"/> Запомнить меня
                    </label>
                </div>
                <button className="w-100 btn btn-lg btn-primary" onClick={login} type="button">
                    Вход
                </button>
            </form>
        </main>
        </div>
    );
}

export default LoginForm;
