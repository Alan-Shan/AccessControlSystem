import React, {useState, useEffect} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {apiService} from "../services/api";
import {useParams} from "react-router-dom";
import {faSpinner} from "@fortawesome/free-solid-svg-icons";

const SingleUser = () => {
    const props = useParams();
    const [newUser] = useState(!Number.isInteger(Number(props.id)));
    const [user, setUser] = useState({});
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState({type: "", text: ""});
    const [errors, setErrors] = useState({});
    const alertClasses = {success: "alert-success", error: "alert-danger", info: "alert-info"};

    const validateForm = () => {
        setErrors({});
        if (!user.username) {
            setErrors((prevErrors) => ({...prevErrors, username: "Поле обязательно"}));
        }
        if (newUser && !user.password) {
            setErrors((prevErrors) => ({...prevErrors, password: "Поле обязательно"}));
        }
        if (user.password !== user.password2) {
            setErrors((prevErrors) => ({...prevErrors, password: "Пароли не совпадают"}));
        }
        return Object.keys(errors).length === 0;
    };

    const sendForm = async () => {
        setErrors({});
        if (!validateForm()) return;
        try {
            if (newUser) {
                await apiService.addAdmin(user);
                setMessage({type: "success", text: "Пользователь успешно добавлен"});
            } else {
                await apiService.modifyAdmin(user);
                setMessage({type: "success", text: "Пользователь успешно изменен"});
            }
        } catch (e) {
            console.log(e);
            if (e.response && e.response.status === 409) {
                setMessage({type: "error", text: "Пользователь с таким именем уже существует"});
            } else {
                setMessage({type: "error", text: "Произошла ошибка при сохранении пользователя"});
            }
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                if (newUser) {
                    setUser((prevUser) => ({...prevUser, admin_type: "admin"}));
                    setLoading(false);
                    return;
                }
                const response = await apiService.getAdmin(props.id);
                setUser(response.data);
            } catch (e) {
                setMessage({type: "error", text: "Произошла ошибка при загрузке пользователя"});
                console.log(e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [props.id, newUser]);

    const alertClass = alertClasses[message.type];

    return (<div className="h-100 d-flex align-items-center justify-content-center mt-4">
            <div className="container w-auto">
                <h1>Пользователь</h1>
                {loading ? (
                    <div className="d-flex justify-content-center w-100 mt-5 mb-5">
                        <div className="spinner-grow" role="status"></div>
                    </div>
                ) : (
                    <div>
                {message.text && (<div className={`alert ${alertClass}`} role="alert">
                        {message.text}
                    </div>)}
                <form onSubmit={(e) => e.preventDefault()}>
                    <div className="form-group mb-3">
                        <label htmlFor="name">Имя пользователя</label>
                        <input
                            type="text"
                            className="form-control"
                            id="name"
                            placeholder="Имя"
                            value={user.username || ""}
                            onChange={(e) => setUser({...user, username: e.target.value})}
                        />
                        {errors.username && <small className="form-text text-danger">{errors.username}</small>}
                    </div>
                    <div className="form-group mb-3">
                        <label htmlFor="password">Пароль</label>
                        <input
                            type="password"
                            className="form-control"
                            id="password"
                            placeholder="Пароль"
                            value={user.password || ""}
                            onChange={(e) => setUser({...user, password: e.target.value})}
                        />
                        {errors.password && <small className="form-text text-danger">{errors.password}</small>}
                    </div>
                    <div className="form-group mb-3">
                        <label htmlFor="password2">Повторите пароль</label>
                        <input
                            type="password"
                            className="form-control"
                            id="password2"
                            placeholder="Повторите пароль"
                            value={user.password2 || ""}
                            onChange={(e) => setUser({...user, password2: e.target.value})}
                        />
                    </div>
                    <div className="form-group mb-3">
                        <label htmlFor="admin_type">Тип пользователя</label>
                        <select
                            className="form-control"
                            id="admin_type"
                            value={user.admin_type || ""}
                            onChange={(e) => setUser({...user, admin_type: e.target.value})}
                        >
                            <option value="admin">Администратор</option>
                            <option value="super_admin">Господь Бог</option>
                        </select>
                    </div>
                    <button type="submit" className="btn btn-primary" onClick={sendForm}>
                        {newUser ? ("Добавить") : ("Сохранить")}
                    </button>
                </form>
                    </div>
                )}
            </div>
        </div>);
};

export default SingleUser;