#! usr/bin/env perl
if(@ARGV >= 2){
	$outfile = pop @ARGV;
	open FILE,$outfile;
	foreach my $dir(@ARGV){
		$bytes = 0;
		opendir DH, $dir or die "Cannot open directory $dir: $!";
		foreach my $file(readdir DH){
			$bytes += -s $file;
		}
		print FILE "$dir: $bytes total bytes.\n";
		closedir DH;
	}
	close FILE;
}

else{
	print "You must pass one output file name and at least one directory in the command line";
	
}