__author__ = 'roberto'


WEB_XML_SERVLET_TEMPLATE = """
<servlet>
    <display-name>{0:s}</display-name>
    <servlet-name>{0:s}</servlet-name>
    <servlet-class>{1:s}</servlet-class>
    <init-param>
        <param-name>sleep-time-in-seconds</param-name>
        <param-value>10</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>{0:s}</servlet-name>
    <url-pattern>/{0:s}</url-pattern>
</servlet-mapping>
"""


WEB_XML_FILTER_TEMPLATE = """
<filter>
    <display-name>{0:s}</display-name>
    <filter-name>{0:s}</filter-name>
    <filter-class>{1:s}</filter-class>
</filter>
<filter-mapping>
    <filter-name>{0:s}</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
"""

class ServletManager(object):

    def __init__(self, qualified_class_name):
        self.qualified_class_name = qualified_class_name
        self.class_name = qualified_class_name.split(".")[-1]

    def get_web_xml_conf(self):
        return WEB_XML_SERVLET_TEMPLATE.format(self.class_name, self.qualified_class_name)


class FilterManager(object):

    def __init__(self, qualified_class_name):
        self.qualified_class_name = qualified_class_name
        self.class_name = qualified_class_name.split(".")[-1]

    def get_web_xml_conf(self):
        return WEB_XML_FILTER_TEMPLATE.format(self.class_name, self.qualified_class_name)



if __name__ == '__main__':
    print(FilterManager("org.crynet.webtools.filter.BaseFilter").get_web_xml_conf())