$(function () {
    $('#div_id_options').each(function () {
        var $divIdOptions = $(this), counter = 0, suspendUpdates = false;
        $('<div class="form-group" />').insertAfter($divIdOptions).load('_container/', function () {
            $('#id_options').appendTo($('#create_advanced'));
            $('#hint_id_options').appendTo($('#create_advanced'));
            $divIdOptions.remove();

            function mungeFields($node, counter) {
                $node.find('[id]').each(function () {
                    this.id += '___' + counter;
                });

                $node.find('[name]').each(function () {
                    this.name += '___' + counter;
                });

                $node.find('input').each(function () {
                    var requires = $(this).data('requires');
                    if (requires) {
                        $(this).data('requires', $.map(requires.split(/\s+/), function (id) {
                            return id + '___' + counter;
                        }).join(' '));
                    }
                });
            }

            function updateOptions() {
                if (!suspendUpdates) {
                    var options = [];
                    $('.panel:not(.hidden)').each(function () {
                        $inputs = $(this).find('input').clone();
                        $inputs.filter('[name]').each(function () {
                            this.name = this.name.split('___')[0];
                        });
                        options.push({
                            'aligner': $(this).find('.panel-title').text().trim(),
                            'name': $(this).find('.aligner-name').prop('value'),
                            'options': $inputs.serialize()
                        });
                    });
                    $('#id_options').prop('value', JSON.stringify(options));
                }
            }

            function addAligner(aligner, name, options) {
                var currentCounter = counter++;
                var panelId = 'aligner_group_' + currentCounter;
                var $panel = $('#aligner_group_template').clone().removeClass('hidden');
                $panel.find('.panel-collapse').attr('id', panelId);
                $panel.find('.aligner-name').attr('id', panelId + '_name');
                $panel.find('a').attr('href', '#' + panelId).text(aligner);
                $panel.find('label').attr('for', panelId + '_name');
                $panel.find('button').click(function (e) {
                    e.preventDefault();
                    $(this).closest('.panel').slideUp(function () {
                        $(this).remove();
                        updateOptions();
                    });
                    return false;
                });
                $panel.find('.aligner-options').load(aligner + '/', function () {
                    var $alignerOptions = $(this);

                    if (name) {
                        $panel.find('.aligner-name').prop('value', name);
                    }

                    if (options) {
                        // Deserialization requires a form, so we make one
                        // temporarily and parent the aligner options to it.
                        var $children = $alignerOptions.children();
                        var $form = $('<form />').append($children);
                        $form.deserialize(options);
                        $children.appendTo($alignerOptions);
                    }

                    mungeFields($alignerOptions, currentCounter);
                    $alignerOptions.find('input[type="checkbox"], input[type="radio"]').change(function () {
                        $alignerOptions.find('input').each(function () {
                            if (!$(this).data('requires')) {
                                return;
                            }

                            var disabled = false;
                            $.each($(this).data('requires').split(/\s+/), function (i, id) {
                                var $dependency = $alignerOptions.find('#' + id);
                                if ($dependency.prop('disabled') || !$dependency.is(':checked')) {
                                    disabled = true;
                                }
                            });
                            $(this).prop('disabled', disabled);
                        });
                    }).change();
                    $panel.hide().appendTo($('#aligner_group')).slideDown();
                    // This needs to come after we show the new fields,
                    // or the options field won't take this form into
                    // consideration.
                    $panel.find('input').change(updateOptions).change();
                });
            }

            $('#aligner_add').click(function (e) {
                e.preventDefault();
                addAligner($('#aligner_add_type').prop('value'));
                return false;
            });

            // If there's an existing value for "options", recreate the
            // forms accordingly.
            $('#id_options').change(function () {
                suspendUpdates = true;
                $('.panel:not(.hidden)').remove();
                var options = JSON.parse($(this).prop('value'));
                $.each(options, function (i, alignerOptions) {
                    addAligner(alignerOptions.aligner,
                               alignerOptions.name,
                               alignerOptions.options);
                });
                suspendUpdates = false;
            });
            if ($('#id_options').prop('value')) {
                $('#id_options').change();
            }
        });

        $divIdOptions.closest('form').submit(function () {
            // Disable all of the elements inside option containers so
            // that their values don't get redundantly submitted.
            $('#aligner_group input').prop('disabled', true);
            return true;
        });
    });
});
