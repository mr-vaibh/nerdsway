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