import { Link } from 'react-router-dom';

const HomePage = () => {
    return (
        <div className="container my-5">
            <div className="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg">
                <div className="col-lg-7 p-3 p-lg-5 pt-lg-3">
                    <h1 className="display-4 fw-bold lh-1">Добро пожаловать</h1>
                    <p className="lead">Lorem ipsum, blah-blah-blah</p>
                    <div className="d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
                        <Link to="/ApplyForVisit">
                            <button type="button" className="btn btn-primary btn-lg px-4 me-md-2 fw-bold">
                                Подать заявку
                            </button>
                        </Link>
                        <Link to="/Main">
                            <button type="button" className="btn btn-outline-secondary btn-lg px-4">
                                Узнать больше
                            </button>
                        </Link>
                    </div>
                </div>
                <div className="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
                    <img className="rounded-lg-3" src="/building.jpg" alt="" width="700" />
                </div>
            </div>
        </div>
    );
}

export default HomePage;