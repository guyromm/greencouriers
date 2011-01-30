OpenLayers.Map.FreeMapIL=OpenLayers.Class(OpenLayers.Map,{initialize:function(e,c){OpenLayers.Lang.setCode("he");OpenLayers.IMAGE_RELOAD_ATTEMPTS=3;OpenLayers.Map.prototype.initialize.apply(this,arguments);var d=new OpenLayers.Layer.Google("Google Streets",{sphericalMercator:true});this.addLayer(d);if(c.navigable){var b=new OpenLayers.Control.Navigation({zoomWheelEnabled:false});this.addControl(b);b.disableZoomWheel()}var a=new OpenLayers.Layer.WMS("OpenLayers WMS","http://labs.metacarta.com/wms/vmap0",{layers:"basic"});var c={layers:[a],minRatio:8,maxRatio:256};if(!this.getCenter()){this.zoomToMaxExtent()}},controls:[new OpenLayers.Control.Attribution({displayClass:"attribu"})],maxResolution:0.010986328125,numZoomLevels:11,CLASS_NAME:"OpenLayers.Map.FreeMapIL"});var safeArgs={};var DEFAULT_LON=34.765;var DEFAULT_LAT=32.058;function createEmbeddedMap(b,e){params=OpenLayers.Util.getParameters();var c=3;var f=["panzoombar","mouse"];var a=["freemap"];var g="false";safeArgs.centerLat=params.lat?params.lat:DEFAULT_LAT;safeArgs.centerLon=params.lon?params.lon:DEFAULT_LON;safeArgs.zoom=9;safeArgs.marker=params.marker?params.marker:g;var h=new String(params.controls);safeArgs.controls=params.controls?h.split(","):f;var j=new String(params.controls);safeArgs.layers=params.layers?j.split(","):a;safeArgs.data=params.data;embeddedMap=new OpenLayers.Map.FreeMapIL(b,{navigable:e,projection:new OpenLayers.Projection("EPSG:900913"),displayProjection:new OpenLayers.Projection("EPSG:4326"),units:"m",numZoomLevels:18,maxResolution:156543.0339,maxExtent:new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508.34)});if(e){for(var d=0;d<safeArgs.controls.length;d++){switch(safeArgs.controls[d]){case"panzoombar":embeddedMap.addControl(new OpenLayers.Control.PanZoomBar());break;case"panzoom":embeddedMap.addControl(new OpenLayers.Control.PanZoom());break;case"layerswitcher":embeddedMap.addControl(new OpenLayers.Control.LayerSwitcher());break}}}embeddedMap.setCenter(new OpenLayers.LonLat(safeArgs.centerLon,safeArgs.centerLat),safeArgs.zoom);vectors=new OpenLayers.Layer.Vector("Vector Layer");embeddedMap.addLayers([vectors]);return{map:embeddedMap,vectors:vectors}}OpenLayers.Control.Click=OpenLayers.Class(OpenLayers.Control,{defaultHandlerOptions:{single:true,"double":false,pixelTolerance:0,stopSingle:false,stopDouble:false},initialize:function(a){this.handlerOptions=OpenLayers.Util.extend({},this.defaultHandlerOptions);OpenLayers.Control.prototype.initialize.apply(this,arguments);this.handler=new OpenLayers.Handler.Click(this,{click:this.trigger},this.handlerOptions)},trigger:function(b){var a=embeddedMap.getLonLatFromViewPortPx(b.xy);map_clicked(b,a)}});