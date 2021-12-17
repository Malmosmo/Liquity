fetch("/api/single/?fromDate=2021-11-01&toDate=2021-12-17").then(response => {
    return response.json()
}).then(json => {
    let sum = 0
    let series = json.data.map(({ _, date, count }) => ({ x: new Date(new Date(date).toDateString()), y: sum += count }))
    let delIdx = []

    series.reduce((previous, current, index) => {
        if (previous.x.getTime() == current.x.getTime()) {
            previous.y += current.y
            delIdx.push(index)

            return previous
        }
        return current
    })

    delIdx.reverse().forEach(idx => {
        series.splice(idx, 1)
    })

    var options = {
        series: [
            {
                name: "Drinks",
                data: series,
            },
        ],
        chart: {
            type: "area",
            height: 350,
            zoom: {
                enabled: true,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: "smooth",
        },
        title: {
            text: "Your Drinks Over Time",
            align: "left",
        },
        subtitle: {
            text: "Accumulated",
            align: "left",
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            opposite: true,
            min: 0,
        },
        legend: {
            horizontalAlign: "left",
        },
    };

    var chart = new ApexCharts(document.querySelector("#OverviewAccumulatedChart"), options);
    chart.render();
})

fetch("/api/single/?fromDate=2021-11-01&toDate=2021-12-17").then(response => {
    return response.json()
}).then(json => {
    let series = json.data.map(({ _, date, count }) => ({ x: date, y: count }))

    var options = {
        series: [
            {
                name: "Drinks",
                data: series,
            },
        ],
        chart: {
            type: "bar",
            height: 350,
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "55%",
                endingShape: "rounded",
            },
        },
        dataLabels: {
            enabled: false,
        },
        title: {
            text: "Your Drinks Over Time",
            align: "left",
        },
        subtitle: {
            text: "Direct with Zoom",
            align: "left",
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            min: 0,
        },
        fill: {
            opacity: 1.0,
        },
        noData: {
            text: "No Data Here... go get yourself a beer",
            align: "center",
            verticalAlign: "middle",
            offsetX: 0,
            offsetY: 0,
            style: {
                color: undefined,
                fontSize: "2rem",
                fontFamily: undefined,
            },
        },
    };

    var chart = new ApexCharts(document.querySelector("#OverviewColumnChart"), options);
    chart.render();
})

fetch("/api/single/?fromDate=2021-11-01&toDate=2021-12-17").then(response => {
    return response.json()
}).then(json => {
    let series = json.data.map(({ beer, _, count }) => ({ x: beer, y: count }))
    let delIdx = []
    series.reduce((previous, current, index) => {
        if (previous.x == current.x) {
            previous.y += current.y
            delIdx.push(index)

            return previous
        }
        return current
    })

    delIdx.reverse().forEach(idx => {
        series.splice(idx, 1)
    })

    console.log(series)

    var options = {
        series: [
            {
                // name: "Drinks",
                data: series,
            },
        ],
        chart: {
            type: "bar",
            height: 350,
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "55%",
                endingShape: "rounded",
            },
        },
        dataLabels: {
            enabled: false,
        },
        title: {
            text: "Your Drinks Over Time",
            align: "left",
        },
        subtitle: {
            text: "Direct with Zoom",
            align: "left",
        },
        xaxis: {
            type: "category",
        },
        yaxis: {
            min: 0,
        },
        fill: {
            opacity: 1.0,
        },
        noData: {
            text: "No Data Here... go get yourself a beer",
            align: "center",
            verticalAlign: "middle",
            offsetX: 0,
            offsetY: 0,
            style: {
                color: undefined,
                fontSize: "2rem",
                fontFamily: undefined,
            },
        },
    };

    var chart = new ApexCharts(document.querySelector("#OverviewStackedChart"), options);
    chart.render();
})