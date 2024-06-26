document.addEventListener('DOMContentLoaded', function(event) {
    let colHeaders = document.querySelectorAll('.filter');

    colHeaders.forEach((colHeader, index) => {
        console.log('index is: ' + index + ', ' + colHeader.textContent);
        colHeader.appendChild(generateDropdown(index));
    });
});

function generateDropdown(index) {
    let columnData = [];
    let rows = document.querySelectorAll('tr');
    rows.forEach((row, i) => {
        if (i == 0) {
            columnData.push('');
            return;
        }
        let cells = row.getElementsByTagName('td');
        columnData.push(cells[index].innerText);
    });
    // REMOVE DUPLICATES
    let uniqColumnData = [...new Set(columnData)];
    // GENERATE THE SELECT OPTION
    let select = document.createElement('select');

    uniqColumnData.map((data, i) => {
        let option = document.createElement('option');
        option.setAttribute('value', data);

        let optionText = document.createTextNode(data);
        option.appendChild(optionText);

        select.appendChild(option);
    });

    select.setAttribute('id', index);
    select.addEventListener('change', function() {
        filterTable(this.value);
        clearSelect(select.id);
    });

    return select;
}

function clearSelect(id) {
    let selects = document.querySelectorAll('select');
    selects.forEach((select, i) => {
        if (id != i) {
            select.value = '';
        }
    });
}

function filterTable(filter) {
    console.log(filter);
    const table = document.querySelector('#teams-table');
    const rows = table.getElementsByTagName('tr');

    // LOOP THROUGH ALL ROWS EXCEPT FOR HEADERS
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;

        // LOOP THROUGH ALL CELLS WITHIN THE ROW
        for (let j = 0; j < cells.length; j++) {
            const cellText = cells[j].textContent || cells[j].innerText;
            if (cellText == filter || cellText.includes(filter)) {
                found = true;
                break;
            }
        }
        rows[i].style.display = found ? '' : 'none';
    }
}
