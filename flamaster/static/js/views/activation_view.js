// Generated by CoffeeScript 1.3.1
var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

define(['chaplin/view', 'text!templates/activate.hbs'], function(View, template) {
  'use strict';

  var ActivationView;
  return ActivationView = (function(_super) {

    __extends(ActivationView, _super);

    ActivationView.name = 'ActivationView';

    function ActivationView() {
      return ActivationView.__super__.constructor.apply(this, arguments);
    }

    ActivationView.prototype.autoRender = true;

    ActivationView.prototype.containerSelector = "#content";

    ActivationView.prototype.id = "activate";

    ActivationView.template = template;

    ActivationView.prototype.initialize = function(options) {
      if (options.hasOwnProperty('template')) {
        this.template = require(options.template);
      }
      console.log("ActivationView#initialize", options);
      return ActivationView.__super__.initialize.call(this, options);
    };

    ActivationView.prototype.getTemplateData = function() {
      var data;
      data = {
        form: {
          id: 'activate-form',
          method: 'post',
          action: '.'
        }
      };
      return data;
    };

    return ActivationView;

  })(View);
});