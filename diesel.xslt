<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="/root">
        <vehicles>
            <xsl:for-each select="item[fuel='Diesel']">
                <xsl:copy-of select="."/>
            </xsl:for-each>
        </vehicles>
    </xsl:template>
</xsl:stylesheet>

