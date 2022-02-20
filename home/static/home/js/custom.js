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
const modal = document.getElementById("subscribe_modal");
const btn = document.getElementById("subscribe_link");
const span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}