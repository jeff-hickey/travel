class RoomForm extends React.Component {
    constructor(props) {
        super(props);
        const div = document.querySelector('#form');
        let cart_data = (div.dataset.cart ?
            JSON.parse(div.dataset.cart.replace(/'/g, '"')) : {})
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
        console.log(this.state.hotel);
        fetch(`/hotel-rooms/${this.state.hotel}/${this.state.arrival}/${this.state.departure}`)
            .then(response => {
                if (response.status > 400) {
                    console.log('Something went wrong')
                    return this.setState(() => {
                        return {error: "Unable to Load Rooms."};
                    });
                }
                return response.json();
            })
            .then(hotel => {
                console.log(hotel.rooms)
                this.setState(() => {
                    return {
                        rooms: hotel.rooms,
                        amenities: hotel.amenities,
                        loaded: true
                    };
                });
            });
    }

    handleCart(room_id, price) {
        fetch(`/cart/${room_id}/${price}`)
            .then((res) => {
                console.log(res)
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
        alert('Your favorite flavor is: ' + this.state.value);
        event.preventDefault();
    }

    render() {
        return (
            <div className="col-md-12">
                <div className="card bg-pink mb-4 box-shadow">
                    <div className="card-body">
                        <form onSubmit={this.handleSubmit} className="form-inline mt-2">
                            <input type="hidden" id="hotel" value={this.state.hotel_id}/>
                            <div className="form-row">
                                <div className="col-lg-4">
                                    <h6 className="card-text white-shadow-text float-left">Arrival</h6><br/>
                                    <input id="arrival" name="arrival" type="date" value={this.state.arrival}
                                           onChange={this.handleChange}
                                           className="form-control form-control-sm"/>
                                </div>
                                <div className="col-lg-4">
                                    <h6 className="card-text white-shadow-text float-left">Departure</h6>
                                    <input id="departure" name="departure" type="date" value={this.state.departure}
                                           onChange={this.handleChange}
                                           className="form-control form-control-sm"/>
                                </div>
                                <div className="col-lg-4">
                                    <input type="submit" id="search_hotels"
                                           className="btn ml-4 mt-4 btn-sm btn-secondary"
                                           value="Update."/>
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
                                <h5 className="card-title">{room.label}</h5>
                                <p className="card-text">{room.about}</p>
                                <div className="d-flex justify-content-between align-items-center">
                                    <div className="btn-group">
                                        {!(room.id in this.state.cart) &&
                                        <button type="button" onClick={() => this.handleCart(room.id, room.price)}
                                                className="btn btn-sm btn-secondary">Add to Cart

                                        </button>}
                                        {room.available && <p>Room Avaialble</p>}
                                        {!(room.available) && <p>Room NO GO</p>}
                                        {(room.id in this.state.cart) &&
                                        <button type="button" onClick={() => this.handleCart(room.id, room.price)}
                                                className="btn btn-sm btn-outline-secondary">Remove from Cart

                                        </button>}
                                    </div>
                                    <small className="text-muted">9 mins</small>
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