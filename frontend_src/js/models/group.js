var Group = Backbone.Model.extend({
    urlRoot: EVENT_API_GROUPS,

    defaults: {
        'name': 'unknown',
        'description': 'unknown',
        'curator': null,
        'members': null
    }
});