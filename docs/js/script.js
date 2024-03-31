window.onload = function() {
    fetch("data.json")
        .then((response) => response.json())
        .then(processJSON);
};

function processJSON(json) {

    // Update summary
    Object.entries(json['summary']).forEach(([key, value]) => {
        document.getElementById(key).textContent = value.toLocaleString();
    });
    document.getElementById("availability").textContent = get_availability(json['summary']);

    // Generate table
    const data = json['data'];
    const table = document.getElementById("table");
    const tbody = table.getElementsByTagName("tbody")[0];
    Object.values(data).forEach(item => {
        const row = document.createElement("tr");

        const title = document.createElement("td");
        title.textContent = item['title'];
        row.append(title);

        const air_date = document.createElement("td");
        air_date.textContent = item['date'];
        row.append(air_date);

        const links = document.createElement("td");
        const rt_link = document.createElement("a");
        rt_link.textContent = "RT";
        rt_link.href = `https://roosterteeth.com/watch/${item['slug']}`;
        rt_link.target = "_blank";
        rt_link.title = "View on Rooster Teeth";
        rt_link.classList.add("w3-hover-text-red");
        rt_link.setAttribute("data-umami-event", "outbound-link-click");
        rt_link.setAttribute("data-umami-event-link", rt_link.href);
        links.append(rt_link);
        if (item['is_uploaded'] || item['is_removed']) {
            const archive_link = document.createElement("a");
            if (item['is_removed']) {
                archive_link.innerHTML = "<s>Archive</s>";
            } else {
                archive_link.textContent = "Archive";
            }
            archive_link.href = `https://archive.org/details/roosterteeth-${item['id']}`;
            archive_link.target = "_blank";
            archive_link.title = "View on Internet Archive";
            archive_link.classList.add("w3-hover-text-red");
            archive_link.setAttribute("data-umami-event", "outbound-link-click");
            archive_link.setAttribute("data-umami-event-link", archive_link.href);
            links.append(" · ");
            links.append(archive_link);
        }
        row.append(links);

        const first = document.createElement("td");
        first.textContent = item['is_first'] ? "⭐️" : "";
        row.append(first);

        const uploaded = document.createElement("td");
        uploaded.textContent = (item['is_uploaded'] || item['is_removed']) ? "✅" : "❌";
        row.append(uploaded);

        const completed = document.createElement("td");
        completed.textContent = item['is_removed'] ? "❓" : (item['is_complete_upload'] ? "✅" : "❌");
        row.append(completed);

        const removed = document.createElement("td");
        removed.textContent = item['is_removed'] ? "🚨" : "";
        row.append(removed);

        tbody.append(row);
    });

    // Generate Internet Archive search link
    const search_url = new URL("https://archive.org/search/");
    const query = `scanner:"Roosterteeth Website Mirror" AND show_title:"${json['show']}"`;
    search_url.searchParams.append("query", query);
    search_url.searchParams.append("sort", "-date");
    const search = document.getElementById("archive_search");
    search.href = search_url.href;
    search.setAttribute("data-umami-event-link", search.href);

    // Reveal everything once ready
    const elements = document.getElementsByClassName("hidden");
    Array.from(elements).forEach(element => {
        element.classList.remove("hidden");
    });
}

// Calculates percent availability for an item
function get_availability(x) {
    const availability = 100 * (x['uploaded'] - x['incomplete'] - x['removed']) / x['count'];
    return availability.toFixed(2) + "%";
}

function search() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tbody = table.getElementsByTagName("tbody")[0];
    tr = tbody.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
