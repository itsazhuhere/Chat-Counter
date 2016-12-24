#! usr/bin/env perl
print "Enter the paragraph: ";
chomp($paragraph = <>);

$paragraph =~ s/\s*/ /g;
$paragraph =~ s/\.\s*/\.  \\u/g;
$paragraph =~ s/([a-z]+)\./\\L$1\\E\./g;

print $paragraph."\n";
