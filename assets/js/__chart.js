/**
 * General
 */
var accumulatedOverviewChart;
var columnOverviewChart;
var stackedOverviewChart;

function renderChart(config, div) {
    var chart = new ApexCharts(document.querySelector("#" + div), config);
    chart.render();

    return chart;
}

// Overview
function columnData(data) {
    var newData = {};

    for (const element of data) {
        let date = new Date(element.date);
        date.setSeconds(0);
        date.setMinutes(0);

        if (date in newData) {
            newData[date] += element.count;
        } else {
            newData[date] = element.count;
        }
    }

    var series = [];

    for (const [key, value] of Object.entries(newData)) {
        series.push({
            x: key,
            y: value,
        });
    }

    return series;
}

function accumulatedData(data) {
    let totalCount = 0;
    var dateDictionary = {};

    for (const element of data) {
        let date = new Date(element.date);
        date.setSeconds(0);
        date.setMinutes(0);
        date.setHours(0);

        if (date in dateDictionary) {
            dateDictionary[date] += element.count;
        } else {
            dateDictionary[date] = totalCount + element.count;
        }

        totalCount += element.count;
    }

    var series = [];

    for (const [key, value] of Object.entries(dateDictionary)) {
        series.push({
            x: key,
            y: parseInt(value),
        });
    }

    return series;
}

function stackedColumnData(data) {
    var newList = [];

    for (const element of data) {
        let date = new Date(element.date);
        date.setSeconds(0);
        date.setMinutes(0);
        date.setHours(0);

        element.date = date;

        newList.push(element);
    }

    var newData = {};

    for (const element of data) {
        if (element.beer in newData) {
            let Added = false;

            for (var i = 0; i < newData[element.beer].length; i++) {
                if (newData[element.beer][i].x.getTime() === element.date.getTime()) {
                    newData[element.beer][i].y += element.count;
                    Added = true;
                }
            }

            if (!Added) {
                newData[element.beer].push({
                    x: element.date,
                    y: element.count,
                });
            }
        } else {
            newData[element.beer] = [
                {
                    x: element.date,
                    y: element.count,
                },
            ];
        }
    }

    var newNewData = [];

    for (const [key, value] of Object.entries(newData)) {
        newNewData.push({
            name: key,
            data: value,
        });
    }

    return newNewData;
}

// Group
function columnSeries(data) {
    var seriesList = [];

    for (const member of data.data) {
        let series = {
            name: member.name,
            data: columnData(member.drinks),
        };

        seriesList.push(series);
    }

    return seriesList;
}

function accumulatedSeries(data) {
    var seriesList = [];

    for (const member of data.data) {
        let series = {
            name: member.name,
            data: accumulatedData(member.drinks),
        };

        seriesList.push(series);
    }

    return seriesList;
}

/**
 * Overview
 */
function initOverviewCharts() {
    let fromDate = document.getElementById("fromDate").value;
    let toDate = document.getElementById("toDate").value;
    let params = "?toDate=" + toDate + "&fromDate=" + fromDate;

    let callback = (args) => {
        accumulatedOverviewChart = renderAccumulatedOverviewChart(args.data, "OverviewAccumulatedChart");
        columnOverviewChart = renderColumnOverviewChart(args.data, "OverviewColumnChart");
        stackedOverviewChart = renderStackedOverviewChart(args.data, "OverviewStackedChart");
    };

    apiSingleCall(params, callback);
}

function updateOverviewCharts() {
    let fromDate = document.getElementById("fromDate").value;
    let toDate = document.getElementById("toDate").value;
    let params = "?single=true&toDate=" + toDate + "&fromDate=" + fromDate;

    let callback = (args) => {
        accumulatedOverviewChart.updateSeries([
            {
                name: "Drinks",
                data: accumulatedData(args.data),
            },
        ]);

        columnOverviewChart.updateSeries([
            {
                name: "Drinks",
                data: columnData(args.data),
            },
        ]);

        stackedOverviewChart.updateSeries(stackedColumnData(args.data));
    };

    apiCall(params, callback);
}

function renderColumnOverviewChart(data, div) {
    var config = {
        series: [
            {
                name: "Drinks",
                data: columnData(data),
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
        /*tooltip: {
            y: {
                formatter: function (val) {
                    return val;
                },
            },
        },*/
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

    return renderChart(config, div);
}

function renderAccumulatedOverviewChart(data, div) {
    var config = {
        series: [
            {
                name: "Drinks",
                data: accumulatedData(data),
            },
        ],
        chart: {
            type: "area",
            height: 350,
            zoom: {
                enabled: false,
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
        /*tooltip: {
            y: {
                formatter: function (val) {
                    return val;
                },
            },
        },*/
    };

    return renderChart(config, div);
}

function renderStackedOverviewChart(data, div) {
    var config = {
        series: stackedColumnData(data),
        chart: {
            type: "bar",
            height: 350,
            stacked: true,
            stackType: "normal",
            toolbar: {
                show: true,
                tools: {
                    download: true,
                    selection: false,
                    zoom: true,
                    zoomin: false,
                    zoomout: false,
                    pan: false,
                    reset: true,
                },
            },
            zoom: {
                enabled: true,
            },
        },
        dataLabels: {
            enabled: false,
        },
        theme: {
            mode: "light",
            palette: "palette1",
        },
        responsive: [
            {
                breakpoint: 480,
                options: {
                    legend: {
                        position: "bottom",
                        offsetX: -10,
                        offsetY: 0,
                    },
                },
            },
        ],
        plotOptions: {
            bar: {
                // borderRadius: 8,
                horizontal: false,
                // endingShape: "rounded",
            },
        },
        title: {
            text: "Your Drinks Over Time",
            align: "left",
        },
        subtitle: {
            text: "Sorted by Drink",
            align: "left",
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            min: 0,
        },
        legend: {
            position: "right",
            offsetY: 40,
        },
        fill: {
            opacity: 1,
        },
    };

    return renderChart(config, div);
}

/**
 * Group
 */
function initGroupCharts(pk) {
    let params = "?grouppk=" + pk;

    let callback = (args) => {
        renderColumnGroupChart(args.data, "GroupColumnChart");
        renderAccumulatedGroupChart(args.data, "GroupAccumulatedChart");
    };

    apiGroupCall(params, callback);
}

function renderColumnGroupChart(data, div) {
    var config = {
        series: columnSeries(data),
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
        stroke: {
            show: true,
            width: 2,
            colors: ["transparent"],
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            title: {
                text: "Drinks",
            },
            min: 0,
        },
        title: {
            text: "Group Drinks Over Time",
            align: "left",
        },
        subtitle: {
            text: "by user",
            align: "left",
        },
        fill: {
            opacity: 1,
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + " Drinks";
                },
            },
        },
    };

    renderChart(config, div);
}

function renderAccumulatedGroupChart(data, div) {
    var config = {
        series: accumulatedSeries(data),
        chart: {
            type: "area",
            height: 350,
            zoom: {
                enabled: false,
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
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + " Drinks";
                },
            },
        },
    };

    renderChart(config, div);
}
