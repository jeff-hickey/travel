document.addEventListener('DOMContentLoaded', function () {
    // Use buttons to toggle between views
    document.querySelector('#booking_form').onsubmit = () => {
        // If first name, last name or phone fields are empty, mark as invalid and return false.
        let invalid = true;
        const first = document.querySelector('#id_first_name');
        first.className = (!first.value ? 'form-control is-invalid' : "form-control is-valid'");

        const last = document.querySelector('#id_last_name');
        last.className = (!last.value ? 'form-control is-invalid' : "form-control is-valid'");

        const phone = document.querySelector('#id_phone');
        phone.className = (!phone.value ? 'form-control is-invalid' : "form-control is-valid'");
        invalid = (!first.value || !last.value || !phone.value);
        return !invalid;
    }
});