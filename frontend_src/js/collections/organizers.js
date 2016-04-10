var Organizers = Backbone.Collection.extend({
    model: User,
    url: EVENT_API_ORGANIZERS,

    parse: function (response) {
        return response.results;
    },

    comparator: function (item) {
        return [item.get('firstName') + item.get('lastName') + item.get('middleName')];
    },

    search: function (letters) {
        var pattern = new RegExp(letters,'gi');
        return (this.filter(function (item) {
            return pattern.test(item.get('firstName') + item.get('lastName') + item.get('middleName'));
        }));
    }
});