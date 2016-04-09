var Group = Backbone.Model.extend({
    urlRoot: "{% url 'group-list' %}",

    defaults: {
        'name': 'unknown',
        'description': 'unknown',
        'curator': null,
        'members': null
    }
});