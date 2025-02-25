document.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('select');
    select.onchange = function() {
        const hello = document.querySelector('#hello');
        hello.style.color = this.value;
    }
});
