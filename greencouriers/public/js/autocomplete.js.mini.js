var AutoComplete=Class.create();AutoComplete.prototype={Version:"1.3.0",REQUIRED_PROTOTYPE:"1.6.0",initialize:function(e,d){this.PROTOTYPE_CHECK();this.fld=$(e);if(!this.fld){throw ("AutoComplete requires a field id to initialize")}this.sInp="";this.nInpC=0;this.aSug=[];this.iHigh=0;this.options=d?d:{};var a,b={valueSep:null,minchars:1,meth:"get",varname:"input",className:"autocomplete",timeout:3000,delay:500,offsety:-5,shownoresults:true,noresults:"No results were found.",maxheight:250,cache:true,maxentries:25,onAjaxError:null,setWidth:false,minWidth:100,maxWidth:200,useNotifier:true};for(a in b){if(typeof(this.options[a])!=typeof(b[a])){this.options[a]=b[a]}}if(this.options.useNotifier){this.fld.addClassName("ac_field")}var c=this;this.fld.onkeypress=function(f){return c.onKeyPress(f)};this.fld.onkeyup=function(f){return c.onKeyUp(f)};this.fld.onblur=function(f){c.resetTimeout();return true};this.fld.setAttribute("AutoComplete","off")},convertVersionString:function(a){var b=a.split(".");return parseInt(b[0])*100000+parseInt(b[1])*1000+parseInt(b[2])},PROTOTYPE_CHECK:function(){if((typeof Prototype=="undefined")||(typeof Element=="undefined")||(typeof Element.Methods=="undefined")||(this.convertVersionString(Prototype.Version)<this.convertVersionString(this.REQUIRED_PROTOTYPE))){throw ("AutoComplete requires the Prototype JavaScript framework >= "+this.REQUIRED_PROTOTYPE)}},onKeyPress:function(b){if(!b){b=window.event}var a=b.keyCode||b.wich;switch(a){case Event.KEY_RETURN:this.setHighlightedValue();Event.stop(b);break;case Event.KEY_TAB:this.setHighlightedValue();break;case Event.KEY_ESC:this.clearSuggestions();break}return true},onKeyUp:function(b){if(!b){b=window.event}var a=b.keyCode||b.wich;if(a==Event.KEY_UP||a==Event.KEY_DOWN){this.changeHighlight(a);Event.stop(b)}else{this.getSuggestions(this.fld.value)}return true},getSuggestions:function(f){if(f==this.sInp){return false}if($(this.acID)){$(this.acID).remove()}this.sInp=f;if(f.length<this.options.minchars){this.aSug=[];this.nInpC=f.length;return false}var c=this.nInpC;this.nInpC=f.length?f.length:0;var b=this.aSug.length;if(this.options.cache&&(this.nInpC>c)&&b&&(b<this.options.maxentries)){var a=new Array();for(var d=0;d<b;d++){if(this.aSug[d].value.toLowerCase().indexOf(f.toLowerCase())!=-1){a.push(this.aSug[d])}}this.aSug=a;this.createList(this.aSug)}else{var e=this;clearTimeout(this.ajID);this.ajID=setTimeout(function(){e.doAjaxRequest(e.sInp)},this.options.delay)}document.helper=this;return false},getLastInput:function(c){var b=c;if(undefined!=this.options.valueSep){var a=b.lastIndexOf(this.options.valueSep);b=a==-1?b:b.substring(a+1,b.length)}return b},doAjaxRequest:function(b){if(b!=this.fld.value){return false}this.sInp=this.getLastInput(this.sInp);if(typeof this.options.script=="function"){var d=this.options.script(encodeURIComponent(this.sInp))}else{var d=this.options.script+this.options.varname+"="+encodeURIComponent(this.sInp)}if(!d){return false}var e=this;var a=this.options.meth;if(this.options.useNotifier){this.fld.removeClassName("ac_field");this.fld.addClassName("ac_field_busy")}var c={method:a,onSuccess:function(f){if(e.options.useNotifier){e.fld.removeClassName("ac_field_busy");e.fld.addClassName("ac_field")}e.setSuggestions(f,b)},onFailure:(typeof e.options.onAjaxError=="function")?function(f){if(e.options.useNotifier){e.fld.removeClassName("ac_field_busy");e.fld.addClassName("ac_field")}e.options.onAjaxError(f)}:function(f){if(e.options.useNotifier){e.fld.removeClassName("ac_field_busy");e.fld.addClassName("ac_field")}}};new Ajax.Request(d,c)},setSuggestions:function(req,input){if(input!=this.fld.value){return false}this.aSug=[];if(this.options.json){var jsondata=eval("("+req.responseText+")");this.aSug=jsondata.results}else{var results=req.responseXML.getElementsByTagName("results")[0].childNodes;for(var i=0;i<results.length;i++){if(results[i].hasChildNodes()){this.aSug.push({id:results[i].getAttribute("id"),value:results[i].childNodes[0].nodeValue,info:results[i].getAttribute("info")})}}}this.acID="ac_"+this.fld.id;this.createList(this.aSug)},createDOMElement:function(g,c,b,f){var h=document.createElement(g);if(!h){return 0}for(var d in c){h[d]=c[d]}var e=typeof(b);if(e=="string"&&!f){h.appendChild(document.createTextNode(b))}else{if(e=="string"&&f){h.innerHTML=b}else{if(e=="object"){h.appendChild(b)}}}return h},createList:function(b){if($(this.acID)){$(this.acID).remove()}this.killTimeout();if(b.length==0&&!this.options.shownoresults){return false}var o=this.createDOMElement("div",{id:this.acID,className:this.options.className});var d=this.createDOMElement("div",{className:"ac_corner"});var g=this.createDOMElement("div",{className:"ac_bar"});var v=this.createDOMElement("div",{className:"ac_header"});v.appendChild(d);v.appendChild(g);o.appendChild(v);var n=this.createDOMElement("ul",{id:"ac_ul"});var r=this;if(b.length==0&&this.options.shownoresults){var m=this.createDOMElement("li",{className:"ac_warning"},this.options.noresults);n.appendChild(m)}else{for(var x=0,t=b.length;x<t;x++){var C=b[x].value;var s=C.toLowerCase().indexOf(this.sInp.toLowerCase());var j=C.substring(0,s)+"<em>"+C.substring(s,s+this.sInp.length)+"</em>"+C.substring(s+this.sInp.length);var u=this.createDOMElement("span",{},j,true);if(b[x].info!=""){var z=this.createDOMElement("br",{});u.appendChild(z);var h=this.createDOMElement("small",{},b[x].info);u.appendChild(h)}var A=this.createDOMElement("a",{href:"#"});var e=this.createDOMElement("span",{className:"tl"},"&nbsp;",true);var c=this.createDOMElement("span",{className:"tr"},"&nbsp;",true);A.appendChild(e);A.appendChild(c);A.appendChild(u);A.name=x+1;A.onclick=function(){r.setHighlightedValue();return false};A.onmouseover=function(){r.setHighlight(this.name)};var m=this.createDOMElement("li",{},A);n.appendChild(m)}}o.appendChild(n);var y=this.createDOMElement("div",{className:"ac_corner"});var B=this.createDOMElement("div",{className:"ac_bar"});var q=this.createDOMElement("div",{className:"ac_footer"});q.appendChild(y);q.appendChild(B);o.appendChild(q);var f=this.fld.cumulativeOffset();o.style.left=f[0]+"px";o.style.top=f[1]+this.fld.offsetHeight+"px";var k=(this.options.setWidth&&this.fld.offsetWidth<this.options.minWidth)?this.options.minWidth:(this.options.setWidth&&this.fld.offsetWidth>this.options.maxWidth)?this.options.maxWidth:this.fld.offsetWidth;o.style.width=k+"px";o.onmouseover=function(){r.killTimeout()};o.onmouseout=function(){r.resetTimeout()};document.getElementsByTagName("body")[0].appendChild(o);this.iHigh=1;this.setHighlight(1);this.toID=setTimeout(function(){r.clearSuggestions()},this.options.timeout)},changeHighlight:function(a){var b=$("ac_ul");if(!b){return false}var c;c=(a==Event.KEY_DOWN||a==Event.KEY_TAB)?this.iHigh+1:this.iHigh-1;c=(c>b.childNodes.length)?b.childNodes.length:((c<1)?1:c);this.setHighlight(c)},setHighlight:function(b){var a=$("ac_ul");if(!a){return false}if(this.iHigh>0){this.clearHighlight()}this.iHigh=Number(b);a.childNodes[this.iHigh-1].className="ac_highlight";this.killTimeout()},clearHighlight:function(){var a=$("ac_ul");if(!a){return false}if(this.iHigh>0){a.childNodes[this.iHigh-1].className="";this.iHigh=0}},setHighlightedValue:function(){if(this.iHigh){if(!this.aSug[this.iHigh-1]){return}if(undefined!=this.options.valueSep){var b=this.getLastInput(this.fld.value);var a=this.fld.value.lastIndexOf(b);b=this.aSug[this.iHigh-1].value+this.options.valueSep;this.sInp=this.fld.value=a==-1?b:this.fld.value.substring(0,a)+b}else{var b=this.getLastInput(this.fld.value);var a=this.fld.value.lastIndexOf(b);b=this.aSug[this.iHigh-1].value;this.sInp=this.fld.value=a==-1?b:this.fld.value.substring(0,a)+b}this.fld.focus();if(this.fld.selectionStart){this.fld.setSelectionRange(this.sInp.length,this.sInp.length)}this.clearSuggestions();if(typeof this.options.callback=="function"){this.options.callback(this.aSug[this.iHigh-1])}}},killTimeout:function(){clearTimeout(this.toID)},resetTimeout:function(){this.killTimeout();var a=this;this.toID=setTimeout(function(){a.clearSuggestions()},a.options.timeout)},clearSuggestions:function(){this.killTimeout();if($(this.acID)){this.fadeOut(300,function(){$(this.acID).remove()})}},fadeOut:function(a,c){this._fadeFrom=1;this._fadeTo=0;this._afterUpdateInternal=c;this._fadeDuration=a;this._fadeInterval=50;this._fadeTime=0;var b=this;this._fadeIntervalID=setInterval(function(){b._changeOpacity()},this._fadeInterval)},_changeOpacity:function(){if(!$(this.acID)){this._fadeIntervalID=clearInterval(this._fadeIntervalID);return}this._fadeTime+=this._fadeInterval;var b=Math.round((this._fadeFrom+((this._fadeTo-this._fadeFrom)*(this._fadeTime/this._fadeDuration)))*100);var d=b/100;var a=$(this.acID);if(a.filters){try{a.filters.item("DXImageTransform.Microsoft.Alpha").opacity=b}catch(c){a.style.filter="progid:DXImageTransform.Microsoft.Alpha(opacity="+b+")"}}else{a.style.opacity=d}if(this._fadeTime>=this._fadeDuration){clearInterval(this._fadeIntervalID);if(typeof this._afterUpdateInternal=="function"){this._afterUpdateInternal()}}}};