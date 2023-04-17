import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {apiService} from '../services/api';
import {faCoffee, faUserEdit, faUserMinus, faUserPlus} from "@fortawesome/free-solid-svg-icons";

const UsersList = () => {
    const history = useNavigate();
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState({ text: '', isError: false });

    const alertClass = message.isError ? 'alert-danger' : 'alert-success';

    useEffect(() => {
        const getUsers = async () => {
            try {
                const response = await apiService.getAdmins();
                setUsers(response.data);
            } catch (e) {
                setMessage({ text: 'Ошибка при получении списка пользователей', isError: true });
            } finally {
                setLoading(false);
            }
        };
        getUsers();
    }, []);

    const editUser = (id) => {
        history(`/users/${id}`);
    };

    const deleteUser = async (id) => {
        try {
            await apiService.deleteAdmin(id);
            setUsers(users.filter((user) => user.id !== id));
            setMessage({ text: 'Пользователь успешно удален', isError: false });
        } catch (e) {
            setMessage({ text: 'Ошибка при удалении пользователя', isError: true });
        }
    };

    return (
        <div className="container mt-4">
            <div className="row">
                <div className="col-md-12">
                    <h1>Список пользователей</h1>
                    {loading && (
                        <div className="d-flex justify-content-center w-100 mt-5 mb-5">
                            <div className="spinner-grow" role="status"></div>
                        </div>
                    )}
                    {message.text && (
                        <div className={`alert ${alertClass}`} role="alert">
                            {message.text}
                        </div>
                    )}
                    {!loading && (
                        <table className="table table-striped">
                            <thead>
                            <tr>
                                <th scope="col">Имя пользователя</th>
                                <th scope="col">Тип</th>
                                <th scope="col">Действия</th>
                            </tr>
                            </thead>
                            <tbody>
                            {users.map((user) => (
                                <tr key={user.id}>
                                    <td>{user.username}</td>
                                    <td>{user.admin_type === 'admin' ? 'Администратор' : 'Господь Бог'}</td>
                                    <td>
                                        <div className="btn-group" role="group">
                                            <button type="button" className="btn btn-primary" onClick={() => editUser(user.id)}>
                                                <FontAwesomeIcon icon={faUserEdit} />
                                            </button>
                                            <button type="button" className="btn btn-danger" onClick={() => deleteUser(user.id)}>
                                                <FontAwesomeIcon icon={faUserMinus} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    )}
                    <button className="btn btn-primary" onClick={() => editUser(null)}>
                        <FontAwesomeIcon className={'me-2'} icon= {faUserPlus} />
                        Добавить пользователя
                    </button>
                </div>
            </div>
        </div>
    );
};

export default UsersList;