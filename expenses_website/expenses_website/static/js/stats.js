

const getChartData=()=>{
    fetch('/expense-category-summary')
    .then(res=>res.json())
    .then((response)=>{
        console.log("response",response);
        const category_data = response.expense_category_data;
        // const mang_rong = [];
        // Lấy danh sách các cặp key-value từ đối tượng category_data và thêm vào mảng rỗng
        // Object.entries(category_data).forEach(([key, value]) => {
        //   mang_rong.push({ category: key, amount: value });
        // });

        // Hiển thị mảng rỗng sau khi đã thêm dữ liệu từ category_data
        // console.log(mang_rong);
        am5.ready(function() {

            // Create root element
            // https://www.amcharts.com/docs/v5/getting-started/#Root_element
            var root = am5.Root.new("chartdiv");
            
            // Set themes
            // https://www.amcharts.com/docs/v5/concepts/themes/
            root.setThemes([
              am5themes_Animated.new(root)
            ]);
            
            // Create chart
            // https://www.amcharts.com/docs/v5/charts/xy-chart/
            var chart = root.container.children.push(am5xy.XYChart.new(root, {
              panX: true,
              panY: true,
              wheelX: "panX",
              wheelY: "zoomX",
              pinchZoomX: true,
              paddingLeft:0,
              paddingRight:1
            }));
            
            // Add cursor
            // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
            var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
            cursor.lineY.set("visible", false);
            
            
            // Create axes
            // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
            var xRenderer = am5xy.AxisRendererX.new(root, { 
              minGridDistance: 30, 
              minorGridEnabled: true
            });
            
            xRenderer.labels.template.setAll({
              rotation: -90,
              centerY: am5.p50,
              centerX: am5.p100,
              paddingRight: 15
            });
            
            xRenderer.grid.template.setAll({
              location: 1
            })
            
            var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
              maxDeviation: 0.3,
              categoryField: "category",
              renderer: xRenderer,
              tooltip: am5.Tooltip.new(root, {})
            }));
            
            var yRenderer = am5xy.AxisRendererY.new(root, {
              strokeOpacity: 0.1
            })
            
            var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
              maxDeviation: 0.3,
              renderer: yRenderer,
              min:0
            }));
            
            // Create series
            // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
            var series = chart.series.push(am5xy.ColumnSeries.new(root, {
              name: "Series 1",
              xAxis: xAxis,
              yAxis: yAxis,
              valueYField: "amount",
              sequencedInterpolation: true,
              categoryXField: "category",
              tooltip: am5.Tooltip.new(root, {
                labelText: "{valueY}"
              })
            }));
            
            series.columns.template.setAll({ cornerRadiusTL: 5, cornerRadiusTR: 5, strokeOpacity: 0 });
            series.columns.template.adapters.add("fill", function (fill, target) {
              return chart.get("colors").getIndex(series.columns.indexOf(target));
            });
            
            series.columns.template.adapters.add("stroke", function (stroke, target) {
              return chart.get("colors").getIndex(series.columns.indexOf(target));
            });
            
            
            // Set data
            // var data = [{
            //   country: "USA",
            //   value: 2025
            // }, {
            //   country: "China",
            //   value: 1882
            // }, {
            //   country: "Japan",
            //   value: 1809
            // }, {
            //   country: "Germany",
            //   value: 1322
            // }, {
            //   country: "UK",
            //   value: 1122
            // }, {
            //   country: "France",
            //   value: 1114
            // }, {
            //   country: "India",
            //   value: 984
            // }, {
            //   country: "Spain",
            //   value: 711
            // }, {
            //   country: "Netherlands",
            //   value: 665
            // }, {
            //   country: "South Korea",
            //   value: 443
            // }, {
            //   country: "Canada",
            //   value: 441
            // }];
            // var chart_data = {};
            // for(var i = 0; i < response.expense_category_data.length; i++)
            // {
            // chart_data.push({ 
            // "category" : response.expense_category_data[i].category,
            // "value"  : parseFloat(response.expense_category_data[i].value)
            // });
            // }
            
            // console.log(chart_data);
            var data = [];
            Object.entries(category_data).forEach(([key,value]) => {
              data.push({category:key, amount:value});
            });
            console.log('data', data);
            xAxis.data.setAll(data);
            series.data.setAll(data);
            
            
            // Make stuff animate on load
            // https://www.amcharts.com/docs/v5/concepts/animations/
            series.appear(1000);
            chart.appear(1000, 100);
            
            }); // end am5.ready()
    });
}

document.onload = getChartData();


