OpenLayers.Map.FreeMapIL = OpenLayers.Class(OpenLayers.Map,{
    initialize: function(div,options) {
	OpenLayers.Lang.setCode("he");
	OpenLayers.IMAGE_RELOAD_ATTEMPTS=3;
	OpenLayers.Map.prototype.initialize.apply(this,arguments);
	this.maxExtent = new OpenLayers.Bounds(33.75,28.125,36.5625,33.75);
	var layer = new OpenLayers.Layer.WMS(OpenLayers.Lang.translate('israel-base'),
	      [ "http://t5.maps.freemap.co.il/wms-c/", 
	      "http://t6.maps.freemap.co.il/wms-c/", 
	      "http://t7.maps.freemap.co.il/wms-c/", 
	      "http://t8.maps.freemap.co.il/wms-c/"
	      ], 
	      {layers: 'base', format: 'image/png' },
	    {'attribution':'<a href="http://www.freemap.co.il">המפה באדיבות WAZE - קהילת הנהגים של ישראל</a>'});
        /*var gmap = new OpenLayers.Layer.Google(
            "Google Streets" // the default
            ,{numZoomLevels: 17}
        );
	this.addLayer(gmap);*/
	this.addLayer(layer);
	
	if (options.navigable)
	{
	    var navctl = new OpenLayers.Control.Navigation({'zoomWheelEnabled': false})
	    this.addControl(navctl);
	    navctl.disableZoomWheel();

	}


	  var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
	      "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
	  var options = {
	      layers: [wms],
	      minRatio: 8,
	      maxRatio: 256
	  };
	/*var overview = new OpenLayers.Control.OverviewMap(options);
	  this.addControl(overview);*/
	if (!this.getCenter()) this.zoomToMaxExtent();
    },
    controls:[new OpenLayers.Control.Attribution({displayClass:'attribu'})],
    maxResolution: .010986328125,
    numZoomLevels: 11,
    CLASS_NAME: "OpenLayers.Map.FreeMapIL"
});

//var embeddedMap,vectors;
var safeArgs = {}
var DEFAULT_LON = 34.765;
var DEFAULT_LAT = 32.058;
function createEmbeddedMap(el,navigable) {
    params = OpenLayers.Util.getParameters();
    var DEFAULT_ZOOM_LEVEL = 3;
    var DEFAULT_CONTROLS = ['panzoombar','mouse'];
    var DEFAULT_LAYERS = ['freemap'];
    var DEFAULT_MARK_CENTER = "false";
    safeArgs.centerLat = params.lat ?         params.lat : DEFAULT_LAT;
    safeArgs.centerLon = params.lon ?         params.lon : DEFAULT_LON;
    safeArgs.zoom = params.zoom ? parseInt(params.zoom) : DEFAULT_ZOOM_LEVEL;
    safeArgs.marker =  params.marker ? params.marker : DEFAULT_MARK_CENTER;
    var controlsStr = new String(params.controls);
    safeArgs.controls = params.controls ? controlsStr.split(",") : DEFAULT_CONTROLS;
    var layersStr = new String(params.controls);
    safeArgs.layers = params.layers ? layersStr.split(",") : DEFAULT_LAYERS;
    safeArgs.data = params.data;
    embeddedMap = new OpenLayers.Map.FreeMapIL(el,{navigable:navigable});

    if (navigable) {
	for(var i = 0; i < safeArgs.controls.length; i++) {
        switch(safeArgs.controls[i]) {
            case 'panzoombar':
                embeddedMap.addControl(new OpenLayers.Control.PanZoomBar());
                break;
            case 'panzoom':
                embeddedMap.addControl(new OpenLayers.Control.PanZoom());
                break;
            case 'layerswitcher':
                embeddedMap.addControl(new OpenLayers.Control.LayerSwitcher());
                break;
        /*case 'mouse':
                embeddedMap.addControl(new OpenLayers.Control.MouseDefaults());
                break;*/
        }
    }
    }
    embeddedMap.setCenter(new OpenLayers.LonLat(safeArgs.centerLon, safeArgs.centerLat), safeArgs.zoom);

    vectors = new OpenLayers.Layer.Vector("Vector Layer");
    //alert('creating');


    embeddedMap.addLayers([vectors]);    
    return {map:embeddedMap,vectors:vectors}
}

OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
    defaultHandlerOptions: {
        'single': true,
        'double': false,
        'pixelTolerance': 0,
        'stopSingle': false,
        'stopDouble': false
    },
    
    initialize: function(options) {
        this.handlerOptions = OpenLayers.Util.extend(
            {}, this.defaultHandlerOptions
        );
        OpenLayers.Control.prototype.initialize.apply(
            this, arguments
        ); 
        this.handler = new OpenLayers.Handler.Click(
            this, {
                'click': this.trigger
            }, this.handlerOptions
        );
    }, 
    
    trigger: function(e) {
        var lonlat = embeddedMap.getLonLatFromViewPortPx(e.xy);
	map_clicked(e,lonlat);
	//markers_layer.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(lonlat.lon,lonlat.lat)));
    }
});