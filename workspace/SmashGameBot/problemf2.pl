#! usr/bin/env perl
if(@ARGV ==1){
	permissions(@ARGV[0]);
}
else{
	print "Enter only one command line argument.";
}

sub permissions{
	my($dir) = @_;
	$new_permissions = 0700;
	@change_files = (0744);
	opendir(DH, $dir)||"Cannot open $dir.";
	foreach $file(readdir DH){
		$mode = (stat($file))[2]&07777;
		if($mode == $new_permissions){
			push @change_files, $file;
		}
	}
	chmod @change_files;
	
	foreach $newfile()
	
	closedir DH;
}