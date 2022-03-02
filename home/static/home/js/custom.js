// search submits form
const searchForm = document.getElementById('search-form');
const searchField = document.getElementById('search-field');

searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (searchField.value !== '' && searchField.value.length > 3) {
        window.location.href = `/search/${searchField.value}/`;
    } else {
        window.location.href = '?humbleMessage=with-all-due-respect-i-just-wanna-say---please-put-some-effort-and-type-minimum-3-characters-long';
    }
});


// subscribe modal
const subscribe_modal = document.getElementById("subscribe_modal");
const subscribe_link = document.getElementById("subscribe_link");
const subscribe_close = document.getElementById("subscribe_close");

subscribe_link.onclick = function() {
    subscribe_modal.style.display = "block";
}
subscribe_close.onclick = function() {
    subscribe_modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == subscribe_modal) {
        subscribe_modal.style.display = "none";
    }
}