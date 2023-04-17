import React, {useState, useEffect} from "react";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {apiService} from "../services/api";
import {useParams} from "react-router-dom";
import {faSave} from "@fortawesome/free-solid-svg-icons";

const SingleRequest = () => {
    const props = useParams();
    const [request, setRequest] = useState({});
    const [newRequest, setNewRequest] = useState(!Number.isInteger(Number(props.id)));
    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState({});
    const [message, setMessage] = useState({text: "", isError: false});

    const alertClass = message.isError ? "alert-danger" : "alert-success";

    const getRequest = async () => {
        try {
            const response = await apiService.getRequest(props.id);
            setRequest(response.data);
            setLoading(false);
        } catch (e) {
            setMessage({text: "Произошла ошибка при загрузке заявки", isError: true});
            console.log(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (newRequest) {
            setLoading(false);
        } else {
            getRequest();
        }
    }, [getRequest, newRequest]);

    const imageChanged = (e) => {
        setErrors({...errors, image: ""});
        const reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        if (!e.target.files[0].type.match(/image.*/)) {
            setErrors({...errors, image: "Файл не является изображением."});
        } else {
            reader.onload = () => {
                setRequest({...request, base64_image: reader.result});
            };
        }
    };

    const saveRequest = async () => {
        if (newRequest) {
            try {
                const response = await apiService.postApplication(request);
                setMessage({text: "Заявка успешно создана.", isError: false});
                setRequest(response.data);
                setNewRequest(false);
            }
            catch (e) {
                setMessage({text: "Произошла ошибка при создании заявки", isError: true});
                console.log(e);
            }
        }
        else {
            try {
                const response = await apiService.modifyRequest(request);
                setMessage({text: "Заявка успешно сохранена.", isError: false});
                setRequest(response.data);
            } catch (e) {
                setMessage({text: "Произошла ошибка при сохранении заявки", isError: true});
                console.log(e);
            }
        }
    };

    return (<div className="container mt-4 mb-4">
            <div className="row">
                <div className="col">
                    <h1 className="text-center">Заявка</h1>
                    {loading ? (
                        <div className="d-flex justify-content-center w-100 mt-5 mb-5">
                            <div className="spinner-grow" role="status"></div>
                        </div>
                    ) : (
                        <div>
                            {message.text && (
                                <div className={`alert ${alertClass}`} role="alert">
                                    {message.text}
                                </div>
                            )}
                            <form>
                                <div className="form-group mb-3">
                                    <label htmlFor="name">Имя</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="name"
                                        value={request.name}
                                        onChange={(e) =>
                                            setRequest({...request, name: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="surname">Фамилия</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="surname"
                                        value={request.surname}
                                        onChange={(e) =>
                                            setRequest({...request, surname: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="patronymic">Отчество</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="patronymic"
                                        value={request.patronymic}
                                        onChange={(e) =>
                                            setRequest({...request, patronymic: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="email">Email</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        id="email"
                                        value={request.email}
                                        onChange={(e) =>
                                            setRequest({...request, email: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="phone">Телефон</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="phone"
                                        value={request.phone}
                                        onChange={(e) =>
                                            setRequest({...request, phone: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="visitPurpose">Цель визита</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="visitPurpose"
                                        value={request.purpose}
                                        onChange={(e) =>
                                            setRequest({...request, purpose: e.target.value})
                                        }
                                    />
                                </div>
                                <span>Тип докумета</span>
                                <div className="row mb-3">
                                    <div className="form-group col-md-6">
                                        <input
                                            className="me-1"
                                            type="radio"
                                            id="passport"
                                            value="passport"
                                            checked={request.document_type === "passport"}
                                            onChange={(e) =>
                                                setRequest({...request, document_type: e.target.value})
                                            }
                                            name="doc_type"
                                        />
                                        <label htmlFor="passport">Паспорт</label>
                                    </div>
                                    <div className="form-group col-md-6">
                                        <input
                                            className="me-1"
                                            type="radio"
                                            id="drivers_license"
                                            value="drivers_license"
                                            checked={request.document_type === "drivers_license"}
                                            onChange={(e) =>
                                                setRequest({...request, document_type: e.target.value})
                                            }
                                            name="doc_type"
                                        />
                                        <label htmlFor="drivers_license">Водительское удостоверение</label>
                                    </div>
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="documentNumber">Номер документа</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="documentNumber"
                                        value={request.document_number}
                                        onChange={(e) =>
                                            setRequest({...request, document_number: e.target.value})
                                        }
                                    />
                                </div>
                                <div className="form-group mb-3">
                                    <label htmlFor="visitPurpose">Цель визита</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="visitPurpose"
                                        value={request.purpose}
                                        onChange={(e) =>
                                            setRequest({...request, purpose: e.target.value})
                                        }
                                    />
                                </div>
                                <img src={request.base64_image} alt="Фото" className="img-fluid mb-3"/>
                                <div className="form-group mb-3">
                                    <label htmlFor="image">Фото</label>
                                    <input
                                        type="file"
                                        className="form-control"
                                        id="formFile"
                                        onChange={imageChanged}
                                    />
                                    {errors.image && (
                                        <div className="alert alert-danger mt-2" role="alert">
                                            {errors.image}
                                        </div>
                                    )}
                                </div>
                                <div className="d-flex justify-content-between">
                                    <button
                                        type="button"
                                        className="btn btn-primary"
                                        onClick={saveRequest}
                                    >
                                        <FontAwesomeIcon icon={faSave} className="me-1"/>
                                        Сохранить
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default SingleRequest;
