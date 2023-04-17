import {useState} from 'react';

const ApplyForVisit = () => {
    const [surname, setSurname] = useState('');
    const [name, setName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [visitPurpose, setVisitPurpose] = useState('');
    const [document, setDocument] = useState({type: 'passport', number: ''});
    const [consent, setConsent] = useState(false);
    const [message, setMessage] = useState({show: false, isError: false, text: ''});
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleInputChange = (event) => {
        const {id, value} = event.target;
        switch (id) {
            case 'surname':
                setSurname(value);
                break;
            case 'name':
                setName(value);
                break;
            case 'patronymic':
                setPatronymic(value);
                break;
            case 'email':
                setEmail(value);
                break;
            case 'phone':
                setPhone(value);
                break;
            case 'doc_number':
                setDocument({...document, number: value});
                break;
            case 'visit_purpose':
                setVisitPurpose(value);
                break;
            case 'passport':
            case 'drivers_license':
                setDocument({...document, type: value});
                break;
            case 'data_processing_consent':
                setConsent(event.target.checked);
                break;
            default:
                break;
        }
    };

    const validate = () => {
        let formIsValid = true;
        let errors = {};
        if (!surname) {
            formIsValid = false;
            errors.surname = 'Поле обязательно для заполнения';
        }
        if (!name) {
            formIsValid = false;
            errors.name = 'Поле обязательно для заполнения';
        }
        if (!email) {
            formIsValid = false;
            errors.email = 'Поле обязательно для заполнения';
        }
        if (!phone) {
            formIsValid = false;
            errors.phone = 'Поле обязательно для заполнения';
        }
        if (!document.number) {
            formIsValid = false;
            errors.doc_number = 'Поле обязательно для заполнения';
        }
        if (!visitPurpose) {
            formIsValid = false;
            errors.visit_purpose = 'Поле обязательно для заполнения';
        }
        if (!consent) {
            formIsValid = false;
            errors.consent = 'Поле обязательно для заполнения';
        }
        setErrors(errors);
        return formIsValid;
    };

    const sendForm = () => {
        if (validate()) {
            // TODO: send form data to server
            setMessage({show: true, isError: false, text: 'Форма успешно отправлена'});
        } else {
            setMessage({show: true, isError: true, text: 'Пожалуйста, заполните все обязательные поля'});
        }
    };

    return (
        <div className="h-100 d-flex align-items-center justify-content-center mt-4">
            <div className="container w-auto">
                {message.show && (
                    <div className={`alert ${message.isError ? 'alert-danger' : 'alert-success'}`} role="alert">
                        {message.text}
                    </div>
                )}
                <h3 className="mb-5">Заявка на посещение</h3>
                <form>
                    <div className="row">
                        <div className="col-md-6">
                            <h5 className="text-muted">Контактная информация</h5>
                            <div className="form-group mb-3">
                                <label htmlFor="surname">Фамилия</label>
                                <input
                                    type="text"
                                    value={surname}
                                    onChange={(e) => setSurname(e.target.value)}
                                    className="form-control"
                                    id="surname"
                                    placeholder="Иванов"
                                />
                                <small id="surnameErrors" className="form-text text-danger">
                                    {errors.surname}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="name">Имя</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="form-control"
                                    id="name"
                                    placeholder="Иван"
                                />
                                <small id="nameErrors" className="form-text text-danger">
                                    {errors.name}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="patronymic">Отчество</label>
                                <input
                                    type="text"
                                    value={patronymic}
                                    onChange={(e) => setPatronymic(e.target.value)}
                                    className="form-control"
                                    id="patronymic"
                                    placeholder="Иванович"
                                />
                                <small id="patronymicErrors" className="form-text text-danger">
                                    {errors.patronymic}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="email">E-mail</label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="form-control"
                                    id="email"
                                    placeholder="email@ilum.top"
                                />
                                <small id="emailErrors" className="form-text text-danger">
                                    {errors.email}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="phone">Телефон</label>
                                <input
                                    type="tel"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    className="form-control"
                                    id="phone"
                                    placeholder="+71234567890"
                                />
                                <small id="phoneErrors" className="form-text text-danger">
                                    {errors.phone}
                                </small>
                            </div>
                        </div>
                        <div className="col-md-6">
                            <h5 className="text-muted">Документ, удостоверяющий личность</h5>
                            <span>Выберите тип документа</span>
                            <div className="row mb-3">
                                <div className=" form-group col-md-6">
                                    <input className="me-1" type="radio" name="doc_type" id="passport" value="passport"
                                           onChange={handleInputChange}/>
                                    <label htmlFor="passport">Паспорт</label>
                                </div>
                                <div className="form-group col-md-6">
                                    <input className="me-1" type="radio" name="doc_type" id="drivers_license"
                                           value="drivers_license" onChange={handleInputChange}/>
                                    <label htmlFor="drivers_license">Водительское удостоверение</label>
                                </div>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="doc_number">Номер документа</label>
                                <input
                                    type="text"
                                    value={document.number}
                                    onChange={(e) => setDocument({...document, number: e.target.value})}
                                    className="form-control"
                                    id="doc_number"
                                    placeholder="1234 567890"
                                />
                                <small id="doc_numberErrors" className="form-text text-danger">
                                    {errors.doc_number}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <label htmlFor="visit_purpose">Цель посещения</label>
                                <input
                                    type="text"
                                    value={visitPurpose}
                                    onChange={(e) => setVisitPurpose(e.target.value)}
                                    className="form-control"
                                    id="visit_purpose"
                                />
                                <small id="visit_purposeErrors" className="form-text text-danger">
                                    {errors.visit_purpose}
                                </small>
                            </div>
                            <div className="form-group mb-3">
                                <input className="me-1" type="checkbox" name="consent" id="consent" value="consent"
                                       onChange={handleInputChange}/>
                                <label htmlFor="consent">Согласие на обработку персональных данных</label>
                                <small id="consentErrors" className="form-text text-danger">
                                    {errors.consent}
                                </small>
                            </div>
                        </div>
                    </div>
                    <button type="button" className="btn btn-primary" onClick={sendForm} disabled={isSubmitting}>
                        {isSubmitting ?
                            <span className="spinner-grow spinner-grow-sm" role="status" hidden="true"></span> +
                            'Отправка...' : 'Отправить'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ApplyForVisit;