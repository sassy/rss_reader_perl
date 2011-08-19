#!/usr/bin/perl

open(fp, "< list.csv");
%hash;
while ($line = <fp>) {
    ($key, $value) = split(/\,/, $line);
    $hash{$key} = $value;
}
close(fp);
print "Content-type: text/html\n\n";
print "<html><body>";

while (($key, $value) = each(%hash)) {
    print "<a href=\".\/rss_view.cgi\?key=" . $key . "\">";
    print $value;
    print "</a><br />";
}

print "</body></html>";

