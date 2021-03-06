// Generated by CoffeeScript 1.3.1
var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

define(['chaplin/view', 'text!templates/home.hbs'], function(View, template) {
  var IndexView;
  return IndexView = (function(_super) {

    __extends(IndexView, _super);

    IndexView.name = 'IndexView';

    function IndexView() {
      return IndexView.__super__.constructor.apply(this, arguments);
    }

    IndexView.prototype.autoRender = true;

    IndexView.prototype.containerSelector = '#content';

    IndexView.prototype.id = 'home';

    IndexView.template = template;

    return IndexView;

  })(View);
});
