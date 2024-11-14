html_table = f"""
<style>
    .table-container {
            {
            width: 100%;
            height: 600px;
            overflow-x: auto;
            overflow-y: auto;
        }
    }

    table.custom-table {
            {
            border-collapse: collapse;
            width: 100%;
            table-layout: auto;
        }
    }

    th,
    td {
            {
            padding: 12px;
            font-size: 14px;
            max-height: 60px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
    }

    /* Specific styling for boolean columns to reduce width */
    .boolean-column {
            {
            min-width: 50px;
            /* Adjust the width as needed */
            max-width: 70px;
            /* Set maximum width for better control */
            text-align: center;
            /* Center align for checkmarks */
        }
    }

    th {
            {
            padding-bottom: 30px;
        }
    }

    th.rotate-header {
            {
            writing-mode: vertical-rl;
            transform: rotate(189deg);
            vertical-align: bottom;
            text-align: center;
            height: 150px;
            white-space: normal;
            word-wrap: break-word;
            max-width: 500px;
        }
    }

    th.first-column-header {
            {
            writing-mode: horizontal-tb;
            text-align: left;
        }
    }

    td {
            {
            border: 1px solid #dddddd;
            text-align: center;
            font-size: 14px;
        }
    }

    /* Freeze the first column */
    td:first-child,
    th:first-child {
            {
            position: sticky;
            left: 0;
            background-color: #fff;
            z-index: 1;
        }
    }

    /* Freeze the second column */
    td:nth-child(2),
    th:nth-child(2) {
            {
            position: sticky;
            left: 100px;
            background-color: #fff;
            z-index: 1;
        }
    }

    /* Freeze the third column */
    td:nth-child(3),
    th:nth-child(3) {
            {
            position: sticky;
            left: 200px;
            background-color: #fff;
            z-index: 1;
        }
    }
</style>
<div class="table-container">
    <table class="custom-table">
        <thead>
            <tr>
                <th class="first-column-header">{"Entity"}</th>
                <th class="second-column-header">{"Comments"}</th>
                <th class="third-column-header">{"Flagged"}</th>
                {" ".join(f"<th class='rotate-header boolean-column'>{col}</th>" if col in col_boolean_list else f"<th
                    class='rotate-header'>{col}</th>" for col in filtered_df.columns if col not in cols_to_exclude)}
            </tr>
        </thead>
        <tbody>
            {" ".join(
            f"<tr>{''.join(f'<td class=\"boolean-column\">{cell}</td>' if col in col_boolean_list else f'<td>{cell}</td>
                ' for col, cell in zip(filtered_df.columns, row))}</tr>"
            for row in filtered_df.values
            )}
        </tbody>
    </table>
</div>
"""