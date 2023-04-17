import {useState} from 'react';
import {Link} from 'react-router-dom';
import {authStore} from "../store/auth";
import {useNavigate} from "react-router-dom";

const NavigationBar = () => {
    const history = useNavigate();
    const [dropdownIsOpen, setDropdownIsOpen] = useState(false);

    const openOrCloseDropdown = () => {
        setDropdownIsOpen(!dropdownIsOpen);
    };

    const handleLogout = () => {
        authStore.logout();
        history('/login');

    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary bd-navbar sticky-top">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">
                    <img src="/favicon.ico" width="30" height="30" className="d-inline-block align-top" alt=""/>
                    OGate
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNavDropdown"
                    aria-controls="navbarNavDropdown"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul className="navbar-nav me-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">
                                Главная
                            </Link>
                        </li>
                        {authStore.hasPrivilegedAccess && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/home">
                                    Админ-панель
                                </Link>
                            </li>
                        )}
                        {authStore.hasPrivilegedAccess && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/requests">
                                    Заявки
                                </Link>
                            </li>
                        )}
                        {authStore.isSuperAdmin && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/users">
                                    Пользователи
                                </Link>
                            </li>
                        )}
                    </ul>
                    <ul className="navbar-nav">
                        {authStore.user != null && (
                            <li className="nav-item dropdown">
                                <a
                                    className="nav-link dropdown-toggle"
                                    href="#"
                                    id="navbarDropdownMenuLink"
                                    role="button"
                                    data-toggle="dropdown"
                                    aria-haspopup="true"
                                    aria-expanded="false"
                                    onClick={openOrCloseDropdown}
                                >
                                    {authStore.currentUsername} ({authStore.currentRole})
                                </a>
                                <div className={`dropdown-menu${dropdownIsOpen ? ' show' : ''}`}
                                     aria-labelledby="navbarDropdownMenuLink">
                                    <a className="dropdown-item">Настройки</a>
                                    <span className="dropdown-item" onClick={handleLogout}>
                    Выход из системы
                  </span>
                                </div>
                            </li>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default NavigationBar;