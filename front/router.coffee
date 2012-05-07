define ['chaplin/mediator', 'chaplin/lib/route'], (mediator, Route) ->
  'use strict'

  class Router # This class does not inherit from Backbone’s router
    constructor: ->
      @registerRoutes()
      @startHistory()

    registerRoutes: ->

      # ---- THE INTREDASTING PART STARTS: ---- #

      # PageController routes
      @match '', 'page#index'
      @match 'signup', 'page#signup'
      @match 'dashboard', 'page#dashboard'
      @match 'account/activate', 'page#activate'

      # ---- THE INTREDASTING PART ENDS. ---- #

    # Start the Backbone History to start routing
    startHistory: ->
      Backbone.history.start pushState: true

    # Connect an address with a controller action
    # Directly create a Backbone.history route
    match: (pattern, target, options = {}) ->
      # console.debug 'Router#match', pattern, target

      # Create a Backbone history instance (singleton)
      Backbone.history or= new Backbone.History

      # Create a route
      route = new Route pattern, target, options
      console.debug 'created route', route

      # Register the route at the Backbone History instance
      Backbone.history.route route, route.handler

    # Route a given URL path manually, return whether a route matched
    route: (path) =>
      console.debug 'Router#route', path
      # Remove leading hash or slash
      path = path.replace /^(\/#|\/)/, ''
      for handler in Backbone.history.handlers
        if handler.route.test(path)
          handler.callback path, changeURL: true
          return true
      false

    # Change the current URL, add a history entry.
    # Do not trigger any routes (which is Backbone’s
    # default behavior, but added for clarity)
    changeURL: (url) ->
      #console.debug 'Router#navigate', url
      Backbone.history.navigate url, trigger: false
