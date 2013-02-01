from django.conf import settings
from django.forms.widgets import TextInput
from django.utils.safestring import SafeUnicode

try:
    url = settings.STATIC_URL
except AttributeError:
    try:
        url = settings.MEDIA_URL
    except AttributeError:
        url = ''

class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ("{0}color-picker/colorpicker.themes.css".format(url),)
        }
        js  = ("{0}color-picker/colorpicker.min.js".format(url),)

#    input_type = 'color'

    def render_script(self, id):
        return u"""
        <div id="colorpick_{0}" class="cp-small"></div>
        <script type="text/javascript">
            (function($){{
                $(document).ready(function(){{
                    var id = '#{0}';
                    var el = $(id);

                    var cp = ColorPicker(
                        document.getElementById('colorpick_{0}'),
                        function(hex, hsv, rgb) {{
                            el.val(hex);
                            el.css('background-color',hex);
                        }});
                    var default_value = el.val();
                    default_value && cp.setHex( default_value );
                    el.change(function(){{
                        cp.setHex( $(this).val() );
                    }})
                }});
            }})('django' in window ? django.jQuery: jQuery)
        </script>
        """.format(id)

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_{0}".format(name)
        render = super(ColorFieldWidget, self).render(name, value, attrs)
        return SafeUnicode(u"%s%s" % (render, self.render_script(attrs['id'])))