document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#search_form').onsubmit = function () {
        let alert_message = '';
        if (document.querySelector('#search_location').value === '0') {
            alert_message += 'Location is required. ';
        }
        if (document.querySelector('#search_arrival').value === '') {
            alert_message += 'Arrival is required. ';
        }
        if (document.querySelector('#search_departure').value === '') {
            alert_message += 'Departure is required. ';
        }
        if (alert_message.length > 0) {
            alert_message = '<h5>We need more info: </h5><p>' + alert_message + '</p>';
            const alert_div = document.querySelector("#alert_message");
            alert_div.innerHTML = alert_message;
            alert_div.style.display = 'block'
            return false;
        }
        return true;
    }
});