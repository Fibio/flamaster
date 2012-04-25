define ['chaplin/lib/subscriber'], (Subscriber) ->
  'use strict'

  class Model extends Backbone.Model
    # Mixin a Subscriber
    _(Model.prototype).defaults Subscriber

    # This method is used to get the attributes for the view template
    # and might be overwritten by decorators which cannot create a
    # proper `attributes` getter due to ECMAScript 3 limits.
    getAttributes: ->
      @attributes

    # Disposal
    # --------

    disposed: false

    dispose: ->
      return if @disposed
      #console.debug 'Model#dispose', this

      # Fire an event to notify associated collections and views
      @trigger 'dispose', this

      # Unbind all global event handlers
      @unsubscribeAllEvents()

      # Remove the collection reference, attributes and event handlers
      properties = [
        'collection', 'attributes', '_escapedAttributes',
        '_previousAttributes', '_callbacks'
      ]
      delete @[prop] for prop in properties

      # Finished
      #console.debug 'Model#dispose', this, 'finished'
      @disposed = true

      # Your're frozen when your heart’s not open
      Object.freeze? this
