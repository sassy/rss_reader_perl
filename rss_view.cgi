#!/usr/bin/perl

use LWP::UserAgent;
use XML::DOM;
use Encode;

sub view($\%\%) {
    my ($blog_title, $items_data, $items_link) = @_;

print << "HEADER";
Content-type: text/html


<HTML><BODY>
<h1>$blog_title</h1>
HEADER

    while (($key, $value) = each(%$items_data)) {
	print "<a href=\"" . ${$items_link}{$key} . "\">\n";
	print "<h2>" . encode("shift_jis", $key) . "</h2>\n";
	print "</a>\n";
	print "<p>" . encode("shift_jis", $value) . "</p>";
    }

print << "FOOTER"
</BODY></HTML>
FOOTER
}

sub process_query {
    my @url_key = split(/=/, $_[0]);
    my $seed = @url_key[1];

    open(fp, "< list.csv");
    my %hash;
    while ($line = <fp>) {
	($key, $value) = split(/\,/, $line);
	$hash{$key} = $value;
    }
    close(fp);

    return $hash{$seed};
}

$query = $ENV{'QUERY_STRING'};
$url = &process_query($query);

$ua = LWP::UserAgent->new;

$req = HTTP::Request->new('GET', $url);

$res = $ua->request($req);
if ($res->is_success) {
    my $parser = new XML::DOM::Parser;
    my $doc = $parser->parse($res->content);
    my @channels = $doc->getElementsByTagName("channel");
    my @ch_childs = @channels[0]->getChildNodes();
    foreach (@ch_childs) {
	if ($_->getNodeType() == ELEMENT_NODE && $_->getTagName() eq "title") {
	    $blog_title =  encode("shift_jis", $_->getFirstChild->toString);
	}
    }
    my @items = $doc->getElementsByTagName("item");
    %items_data;
    %items_link;
    foreach (@items) {	
	foreach ($_->getChildNodes) {
	    $nname = $_->getNodeName;
	    if ( $nname eq "title")  {
		$title =  $_->getFirstChild->toString;
	    } elsif ($nname eq "description") {
		$desc =  $_->getFirstChild->toString;
	    } elsif ($nname eq "link") {
		$link =  $_->getFirstChild->toString;
	    }
	}
	$items_data{$title} = $desc;
	$items_link{$title} = $link;
    }
} else {
    print "error";
    exit;
}

&view($blog_title, \%items_data, \%items_link);
