define ['chaplin/mediator', 'chaplin/lib/utils'], (mediator, utils) ->

  'use strict'

  # Registers several Handlebars helpers

  prepareAttrs = (attrs) -> ("#{attr}='#{value}'" for attr, value of attrs).join " "
  inputRenderer = (attrs) ->
    "<input #{prepareAttrs(attrs)} id='id_#{attrs.name}' class='input-large' />"
  # Partials
  # --------

  Handlebars.registerHelper 'partial', (partialName, options) ->
    new Handlebars.SafeString(
      Handlebars.VM.invokePartial(
        Handlebars.partials[partialName], partialName, options.hash
      )
    )

  # Generators
  # ----------

  # Facebook image URLs
  Handlebars.registerHelper 'fb_img_url', (fbId, type) ->
    new Handlebars.SafeString utils.facebookImageURL(fbId, type)

  # Conditional evaluation
  # ----------------------

  # Choose block by user login status
  Handlebars.registerHelper 'if_logged_in', (options) ->
    if mediator.user
      options.fn(this)
    else
      options.inverse(this)

  # Map helpers
  # -----------

  # Make 'with' behave a little more mustachey
  Handlebars.registerHelper 'with', (context, options) ->
    if not context or Handlebars.Utils.isEmpty context
      options.inverse(this)
    else
      options.fn(context)

  # Inverse for 'with'
  Handlebars.registerHelper 'without', (context, options) ->
    inverse = options.inverse
    options.inverse = options.fn
    options.fn = inverse
    Handlebars.helpers.with.call(this, context, options)

  # Evaluate block with context being current user
  Handlebars.registerHelper 'with_user', (options) ->
    context = mediator.user or {}
    Handlebars.helpers.with.call(this, context, options)

  # helper for a label for input field
  Handlebars.registerHelper 'labelFor', (name, text) ->
    "<label class='control-label' for='id_#{name}'>#{text}</label>"

  # helper for a text input
  Handlebars.registerHelper 'textField', (name, placeholder) ->
    inputRenderer
      type: 'text'
      name: name
      placeholder: placeholder

  # helper for a password input
  Handlebars.registerHelper 'passwordField', (name, placeholder) ->
    inputRenderer
      type: 'password'
      name: name
      placeholder: placeholder

  # Helper for a form rendering
  Handlebars.registerHelper 'form', (context, options) ->
    attrs = _(@form).defaults(options.hash)
    "<form #{prepareAttrs(attrs)}>#{options.fn(context)}</form>"

  null
