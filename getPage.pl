#!/usr/bin/perl
use LWP::Simple;
use HTML::Parse;

if ($#ARGV==0)
{
    #This is the line that determines which wiki you grab from
    #the plan is to make this customizeable

    #my $url ='http://bulbapedia.bulbagarden.net/wiki/'.$ARGV[0];
    my $url ='http://en.wikipedia.org/wiki/'.$ARGV[0];

    #gets the page contents
    my $ua = LWP::UserAgent->new();
    my $res = $ua->get($url);
    
    #prints the parsed contents
    print parse_html($res->content)->format;
}



