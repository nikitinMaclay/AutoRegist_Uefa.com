<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dynamic Pagination Table with Filtering</title>
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }

    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }

    th {
      background-color: #f2f2f2;
    }

    .pagination {
      display: flex;
      justify-content: center;
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .pagination li {
      display: inline-block;
      margin: 0 4px;
    }

    .pagination a {
      text-decoration: none;
      padding: 8px 12px;
      border: 1px solid #ddd;
      background-color: #f2f2f2;
      color: #333;
      border-radius: 4px;
      cursor: pointer;
    }

    .pagination a.active {
      background-color: #4CAF50;
      color: white;
    }
  </style>
</head>
<body>

  <input type="text" id="filterInput" placeholder="Filter by Name or Email">

  <table id="data-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      <!-- Your data rows here -->
    </tbody>
  </table>

  <ul class="pagination" id="pagination"></ul>

  <script>
    const itemsPerPage = 15;
    let currentPage = 1;
    let filterText = '';

    function displayData(page) {
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const tableBody = document.querySelector('#data-table tbody');
      const rows = tableBody.querySelectorAll('tr');
      rows.forEach((row, index) => {
        const rowData = row.textContent.toLowerCase();
        const filterLowerCase = filterText.toLowerCase();

        if (
          index >= startIndex &&
          index < endIndex &&
          (rowData.includes(filterLowerCase) || filterText === '')
        ) {
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

    function updateFilter() {
      filterText = document.querySelector('#filterInput').value.trim();
      currentPage = 1;
      displayData(currentPage);
      setupPagination();
    }

    // Initial setup
    displayData(currentPage);
    setupPagination();

    // Event listener for input change
    document.querySelector('#filterInput').addEventListener('input', updateFilter);
  </script>

</body>
</html>
