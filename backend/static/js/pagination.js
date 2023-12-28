document.addEventListener("DOMContentLoaded", function() {

    const itemsPerPage = 10;
    let currentPage = 1;

    function displayData(page) {
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const tableBody = document.querySelector('#data-table tbody');
      const rows = tableBody.querySelectorAll('tr');
      rows.forEach((row, index) => {
        if (index >= startIndex && index < endIndex) {
          row.style.display = 'table-row';
        } else {
          row.style.display = 'none';
        }
      });
    }

    function setupPagination() {
      const tableBody = document.querySelector('#data-table tbody');
      const rows = tableBody.querySelectorAll('tr');
      const totalPages = Math.ceil(rows.length / itemsPerPage);
      const pagination = document.querySelector('#pagination');
      pagination.innerHTML = '';

      for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = i;

        if (i === currentPage) {
          link.classList.add('active');
        }

        link.addEventListener('click', (event) => {
          event.preventDefault();
          currentPage = i;
          displayData(currentPage);
          highlightCurrentPage();
        });

        li.appendChild(link);
        pagination.appendChild(li);
      }
    }

    function highlightCurrentPage() {
      const links = document.querySelectorAll('.pagination a');
      links.forEach((link, index) => {
        if (index + 1 === currentPage) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }

    // Initial setup
    displayData(currentPage);
    setupPagination();
});