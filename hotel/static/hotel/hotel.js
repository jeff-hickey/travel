class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            hotel: [],
            rooms: [],
            room: [],
            price: props.price,
            amenities: [],
            loaded: false,
            showBookingForm: false,
            placeholder: "Loading"
        };
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        fetch(`/hotel-info/${document.querySelector('#app').dataset.hotelid}`)
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return {placeholder: "Something went wrong!"};
                    });
                }
                return response.json();
            })
            .then(hotel => {
                console.log(hotel.rooms)
                this.setState(() => {
                    return {
                        hotel,
                        rooms: hotel.rooms,
                        amenities: hotel.amenities,
                        loaded: true
                    };
                });
            });
    }

    handleClick(room) {
        this.setState(state => ({
            room: room.id,
            price: room.price,
            showBookingForm: !this.state.showBookingForm
        }));
    }

    render() {
        return (
            <div>
                <div className="card-body">
                    <a href="#"><h2 className="card-text">{this.state.hotel.label}</h2></a>
                    <div className="card-text"><p className="align-content-start">{this.state.hotel.about_hotel}</p>
                    </div>
                </div>
                <ul className="list-group">
                    {this.state.rooms.map((room) => {
                        return (
                            <li className="list-group-item border-0" key={room.id}>
                                {this.state.showBookingForm && (this.state.room === room.id) &&
                                <div>
                                    <Booking room={this.state.room} price={this.state.price}/>
                                    <h5 className="mt-4">{room.label}</h5>
                                    <p className="text-justify">{room.about}</p>
                                </div>
                                }
                                {!this.state.showBookingForm &&
                                <div>
                                    <h5>{room.label}</h5>
                                    <p className="text-justify">{room.about}</p>
                                    <p className="float-right">
                                        <button className="btn btn-md btn-secondary mt-2" onClick={() => {
                                            this.handleClick(room)
                                        }}>Book now.
                                        </button>
                                    </p>
                                </div>}
                            </li>
                        )
                    })}
                </ul>
            </div>

        );
    }
}

class Booking extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            phone: props.phone,
            full_name: document.querySelector('#app').dataset.fullname,
            arrival: props.arrival,
            departure: props.departure,
            price: props.price,
            room: props.room,
            confirmation: props.confirmation,
            showConfirm: false,
            errors: props.errors,
            showErrors: false
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    handleInputChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    validateForm() {
        let valid = true;
        // Any missing field equals an invalid form.
        if (this.state.full_name === '' || !this.state.arrival
            || !this.state.departure || !this.state.phone) {
            valid = false;
        }
        this.setState({
            errors: (valid ? '' : 'All fields are required.'),
            showErrors: !valid
        });
        return valid;
    }

    handleClick(event) {
        event.preventDefault();
        if (this.validateForm()) {
            fetch('/booking', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
                body: JSON.stringify({
                    price: this.state.price,
                    room: this.state.room,
                    full_name: this.state.full_name,
                    phone: this.state.phone,
                    arrival: this.state.arrival,
                    departure: this.state.departure
                })
            }).then(response => {
                if (!response.ok) {
                    throw Error(response.status + ' - ' + response.statusText);
                }
                return response.json()

            }).then((data) => {
                this.setState({
                    confirmation: data.confirmation,
                    showConfirm: true
                });
            }).catch(console.log)
        }
    }

    render() {
        return (
            <div className="container float-center">
                {this.state.showConfirm &&
                <div className="form-row mb-2">
                    <div className="card w-100">
                        <div className="card-body">
                            <p><a href="#" className="btn btn-lg btn-secondary mt-2">Booked. Your confirmation
                                is: {this.state.confirmation}</a></p>
                            <h5 className="card-title">{this.state.showConfirm && this.state.full_name}</h5>
                            <h6 className="card-subtitle mb-2 text-muted">Phone: {this.state.showConfirm && this.state.phone}</h6>
                            <h6 className="card-subtitle mb-2 text-muted">Arrival: {this.state.showConfirm && this.state.arrival}</h6>
                            <h6 className="card-subtitle mb-2 text-muted"> Departure: {this.state.showConfirm && this.state.departure}</h6>
                        </div>
                    </div>
                </div>}
                {this.state.showErrors && <div className="alert alert-danger" role="alert">{this.state.errors}</div>}
                <div className="form-row">
                    <div className="col">
                        {!this.state.showConfirm && <label> Phone:
                            <input className="form-control" name="phone" type="input" checked={this.state.phone}
                                   onChange={this.handleInputChange}/>
                        </label>}
                    </div>
                    <div className="col">
                        {!this.state.showConfirm && <label>
                            Full Name:
                            <input className="form-control" name="full_name" type="input"
                                   value={this.state.full_name}
                                   checked={this.state.full_name}
                                   onChange={this.handleInputChange}/>
                        </label>}
                    </div>
                </div>
                <div className="form-row">
                    <div className="col">
                        {!this.state.showConfirm && <label>
                            Arrival Date (YYYY-MM-DD):
                            <input className="form-control" name="arrival" type="input" checked={this.state.arrival}
                                   onChange={this.handleInputChange}/>
                        </label>}
                    </div>
                    <div className="col">
                        {!this.state.showConfirm && <label>
                            Departure Date (YYYY-MM-DD):
                            <input className="form-control" name="departure" type="input" checked={this.state.departure}
                                   onChange={this.handleInputChange}/>
                        </label>}
                    </div>
                </div>
                {!this.state.showConfirm && <p className="lead">
                    <button type="submit" onClick={this.handleClick} className="btn btn-lg btn-secondary mt-2">
                        Book this Room.
                    </button>
                </p>}
            </div>
        );
    }
}


ReactDOM.render(<App/>, document.querySelector("#app"));

