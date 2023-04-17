import {useState, useEffect} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {apiService} from "../services/api";
import {useNavigate} from "react-router-dom";
import {faCheck, faPencil, faPlus, faTimes} from "@fortawesome/free-solid-svg-icons";

const RequestsList = () => {
    const history = useNavigate();
    const [requests, setRequests] = useState([]);
    const [message, setMessage] = useState({type: '', text: ''});
    const [loading, setLoading] = useState(true);
    const alertClasses = {
        success: 'alert-success',
        error: 'alert-danger',
        info: 'alert-info',
    };

    useEffect(() => {
        async function fetchRequests() {
            try {
                const response = await apiService.getRequests();
                setRequests(response.data);
                if (!response.data.length) {
                    setMessage({
                        type: 'info',
                        text: 'В данный момент заявки в системе отсутствуют',
                    });
                }
            } catch (e) {
                setMessage({
                    type: 'error',
                    text: 'Произошла ошибка при загрузке заявок',
                });
                console.log(e);
            } finally {
                setLoading(false);
            }
        }

        fetchRequests();
    }, []);

    const alertClass = alertClasses[message.type];

    const redirectToRequest = (id) => {
        history(`/requests/${id}`);
    };

    const addRequest = () => {
        history('/requests/add');
    };

    const requestStatus = (id) => {
        const request = requests.find((request) => request.id === id);
        switch (request.status) {
            case 'approved':
                return 'Принята';
            case 'rejected':
                return 'Отклонена';
            default:
                return 'В обработке';
        }
    };

    const setGenericError = () => {
        setMessage({
            type: 'error',
            text: 'Произошла ошибка.',
        });
    };

    const reject = async (id) => {
        try {
            await apiService.rejectRequest(id);
            setRequests(
                requests.map((request) => {
                    if (request.id === id) {
                        return {...request, status: 'rejected'};
                    }
                    return request;
                })
            );
            setMessage({
                type: 'success',
                text: 'Заявка отклонена.',
            });
        } catch (_) {
            setGenericError();
        }
    };

    const accept = async (id) => {
        try {
            await apiService.approveRequest(id);
            setRequests(
                requests.map((request) => {
                    if (request.id === id) {
                        return {...request, status: 'approved'};
                    }
                    return request;
                })
            );
            setMessage({
                type: 'success',
                text: 'Заявка принята.',
            });
        } catch (_) {
            setGenericError();
        }
    };

    return (
        <div className="container h-100 mt-4">
            <div className="row">
                <div className="col-md-12">
                    <h1>Заявки</h1>
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
                    {!loading && requests.length > 0 && (
                        <table className="table table-responsive table-bordered">
                            <thead>
                            <tr>
                                <th scope="col">ФИО</th>
                                <th scope="col">Email</th>
                                <th scope="col">Телефон</th>
                                <th scope="col">Цель визита</th>
                                <th scope="col">Тип документа</th>
                                <th scope="col">Номер документа</th>
                                <th scope="col">Дата создания</th>
                                <th scope="col">Статус</th>
                                <th scope="col">Действия</th>
                            </tr>
                            </thead>
                            <tbody>
                            {requests.map((request) => (
                                <tr key={request.id}>
                                    <td>
                                        {request.name} {request.surname} {request.patronymic}
                                    </td>
                                    <td>{request.email}</td>
                                    <td>{request.phone}</td>
                                    <td>{request.purpose}</td>
                                    <td>{request.document_type}</td>
                                    <td>{request.document_number}</td>
                                    <td>{request.creation_time}</td>
                                    <td>{requestStatus(request.id)}</td>
                                    <td>
                                        <div className="btn-group" role="group">
                                            <button
                                                type="button"
                                                className="btn btn-primary"
                                                onClick={() => accept(request.id)}
                                            >
                                                <FontAwesomeIcon icon={faCheck}/>
                                            </button>
                                            <button
                                                type="button"
                                                className="btn btn-danger"
                                                onClick={() => reject(request.id)}
                                            >
                                                <FontAwesomeIcon icon={faTimes}/>
                                            </button>
                                            <button
                                                type="button"
                                                className="btn btn-secondary"
                                                onClick={() => redirectToRequest(request.id)}
                                            >
                                                <FontAwesomeIcon icon={faPencil}/>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    )}
                    <button className="btn btn-primary" onClick={() => addRequest(null)}>
                        <FontAwesomeIcon className={"me-2"} icon={faPlus}/>
                        Добавить заявку
                    </button>
                </div>
            </div>
        </div>
    );
}

export default RequestsList;