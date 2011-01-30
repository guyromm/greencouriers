OpenLayers.Map.FreeMapIL = 
  OpenLayers.Class(OpenLayers.Map, 
  {
      initialize: function (div, options){
	  OpenLayers.Lang.setCode("he");
	  OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
	  //call OpenLayers.Map super ...
	  OpenLayers.Map.prototype.initialize.apply(this, arguments);
	  //for some odd reason I can't seem to be able to override mapExtent when my value appears in the options (Map initialize
	  //ignores my value) thus I'll override it here!
	  this.maxExtent =  new OpenLayers.Bounds(33.75,28.125,36.5625,33.75);
	  //add base layer
	  var layer = new OpenLayers.Layer.WMS(OpenLayers.Lang.translate("israel-base"), 
	      [ "http://t5.maps.freemap.co.il/wms-c/", 
	      "http://t6.maps.freemap.co.il/wms-c/", 
	      "http://t7.maps.freemap.co.il/wms-c/", 
	      "http://t8.maps.freemap.co.il/wms-c/"
	      ], 
	      {layers: 'base', format: 'image/png' },
	      {'attribution':'<a href="http://www.freemap.co.il">FreeMap Israel&copy;</a>'});
	  
	  this.addLayer(layer);

	  this.addControl(new OpenLayers.Control.Navigation());
	  //this.addControl(new OpenLayers.Control.Scale());
	  //this.addControl(new OpenLayers.Control.MousePosition());
	  //this.addControl(new OpenLayers.Control.Permalink());
	  //this.addControl(new OpenLayers.Control.LayerSwitcher());
		
	  //add overview layer
	  var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
	      "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
	  var options = {
	      layers: [wms],
	      minRatio: 8,
	      maxRatio: 256
	  };
	  var overview = new OpenLayers.Control.OverviewMap(options);
	  this.addControl(overview);
	  if (!this.getCenter()) this.zoomToMaxExtent();
	},
	
      //add the attribution control before init or the display class will not affect the attrib
      //OpenLayers only so-so ...
      //init other controls in init or IE6 will cry
      controls: [new OpenLayers.Control.Attribution({displayClass:"attrib"})],
      maxResolution: .010986328125,
      
      numZoomLevels: 11,
      
      /** @final @type String */
      CLASS_NAME: "OpenLayers.Map.FreeMapIL"
});

var safeArgs = {}
var embeddedMap,vectors;
var DEFAULT_LON = 34.765;
var DEFAULT_LAT = 32.058;
function createEmbeddedMap(el) {
    OpenLayers.ProxyHost = '/proxy/?url='; 
    // ----
    // TODO: Handle all this parsing better.
    
    //read URL parameters
    params = OpenLayers.Util.getParameters();
    
    var DEFAULT_ZOOM_LEVEL = 3;
    var DEFAULT_CONTROLS = ['panzoombar','mouse'];
    var DEFAULT_LAYERS = ['freemap'];
    var DEFAULT_MARK_CENTER = "false";

    safeArgs.centerLat = params.lat ? 
        params.lat : DEFAULT_LAT;
    
    safeArgs.centerLon = params.lon ? 
        params.lon : DEFAULT_LON;

    safeArgs.zoom = params.zoom ? parseInt(params.zoom) : DEFAULT_ZOOM_LEVEL;
    
    safeArgs.marker =  params.marker ? params.marker : DEFAULT_MARK_CENTER;

    //need to read it to a String or the split below won't work
    var controlsStr = new String(params.controls);
    safeArgs.controls = params.controls ? 
        controlsStr.split(",") : DEFAULT_CONTROLS;
    
     //need to read it to a String or the split below won't work
    var layersStr = new String(params.controls);
    safeArgs.layers = params.layers ? 
        layersStr.split(",") : DEFAULT_LAYERS;

    safeArgs.data = params.data; // TODO: Make this "safe".

    // -----
    embeddedMap = new OpenLayers.Map.FreeMapIL(el);

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
            case 'mouse':
                embeddedMap.addControl(new OpenLayers.Control.MouseDefaults());
                break;
        }
    }

    embeddedMap.setCenter(new OpenLayers.LonLat(safeArgs.centerLon, safeArgs.centerLat), safeArgs.zoom);
    vectors = new OpenLayers.Layer.Vector("Vector Layer");
    embeddedMap.addLayers([vectors]);

    //return ({map:embeddedMap,vectors:vectors});
}