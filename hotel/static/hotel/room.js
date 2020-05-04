class RoomForm extends React.Component {
    constructor(props) {
        super(props);
        const div = document.querySelector('#form');
        let cart_data = (div.dataset.cart ?
            JSON.parse(div.dataset.cart.replace(/'/g, '"')) : {});
        this.state = {
            arrival: div.dataset.arrival,
            departure: div.dataset.departure,
            hotel: div.dataset.hotel,
            cart: cart_data,
            loaded: false
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCart = this.handleCart.bind(this);

    }

    componentDidMount() {
        // Populate the room list.
        this.fetchRooms(this.state.arrival);
        flatpickr(ReactDOM.findDOMNode(this.refs.arrivalPicker), {minDate: "today",});
        flatpickr(ReactDOM.findDOMNode(this.refs.departurePicker), {minDate: new Date().fp_incr(1)});
    }

    fetchRooms(arrival) {
        fetch(`/hotel-rooms/${this.state.hotel}/${this.state.arrival}/${this.state.departure}`)
            .then(response => {
                if (response.status > 400) {
                    console.log('Something went wrong');
                    return this.setState(() => {
                        return {error: "Unable to Load Rooms."};
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        rooms: data.rooms,
                        loaded: true
                    };
                });
            });
    }

    handleCart(room_id, price) {
        fetch(`/cart/${room_id}/${this.state.arrival}/${this.state.departure}/${price}`)
            .then((res) => {
                return res.json()
            })
            .then((result) => {
                // Reload the page to display the cart and remove
                // rooms from availability.
                location.reload();
            }).catch(console.log)
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        event.preventDefault();
        this.setState({
            arrival: this.refs.arrivalPicker.value,
            departure: this.refs.departurePicker.value,
            loaded: false
        }, () => {
            this.fetchRooms(this.state.arrival);
        })
    }

    render() {
        return (
            <div className="col-md-12">
                <div className="card bg-pink mb-4 box-shadow">
                    <div className="card-body">
                        <form onSubmit={this.handleSubmit} className="form-inline mt-2">
                            <input type="hidden" id="hotel" value={this.state.hotel_id}/>
                            <div className="row">
                                <div className="col-lg-4">
                                    <label htmlFor="arrival" className="float-left"><small
                                        className="card-text text-white">Arrival</small></label>
                                    <input id="arrival" ref="arrivalPicker" name="arrival" type="text"
                                           value={this.state.arrival}
                                           onChange={this.handleChange}
                                           className="form-control form-control-sm"/>
                                </div>
                                <div className="col-lg-4">
                                    <label htmlFor="departure" className="float-left"><small
                                        className="card-text text-white">Departure</small></label>
                                    <input id="departure" ref="departurePicker" name="departure" type="text"
                                           value={this.state.departure}
                                           onChange={this.handleChange}
                                           className="form-control form-control-sm"/>
                                </div>
                                <div className="col-lg-4">
                                    <input type="submit" id="search_hotels"
                                           className="btn ml-2 mt-3 btn-md btn-secondary"
                                           value="Update Rooms."/>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                {!this.state.loaded &&
                <div className="d-flex justify-content-center">
                    <div className="spinner-border text-secondary mt-4" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>}
                {this.state.loaded && this.state.rooms.map((room) => {
                    return (
                        <div key={room.id} className="card mb-4 box-shadow">
                            {room.image_url && <img src={room.image_url} className="card-img-top" alt={room.label}/>}
                            <div className="card-body">
                                <h5 className="card-title">{room.label} {room.available}</h5>
                                <p className="card-text">{room.about}</p>
                                <div className="d-flex justify-content-between align-items-center">
                                    <div className="btn-group">
                                        {/* Room is not in cart. */}
                                        {!(room.id in this.state.cart) && room.available &&
                                        <button type="button" onClick={() => this.handleCart(room.id, room.price)}
                                                className="btn btn-md btn-secondary">Add to Cart
                                        </button>}
                                        {!(room.id in this.state.cart) && !(room.available) &&
                                        <h5 className="pink-shadow-text">Not Available.</h5>}
                                        {/* Room is in cart. */}
                                        {(room.id in this.state.cart) &&
                                        <button type="button" onClick={() => this.handleCart(room.id, room.price)}
                                                className="btn btn-md btn-outline-secondary">Remove from Cart

                                        </button>}
                                    </div>
                                    <h4 className="pink-shadow-text">${room.price}</h4>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>
        );
    }
}

ReactDOM.render(<RoomForm/>, document.querySelector("#form"));