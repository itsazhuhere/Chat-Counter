#!/usr/bin/env perl
$file_name = "";
if(! open NAMES, $file_name){
	die "Failed to open file";
}
%names;
while(<NAMES>){
	chomp;
	my ($login,$last_name) = $_ ~= /^([^:]+) #login name group
									:[^:]+	#extraneous sections
									:[^:]+
									:[^:]+
									:([^\s]+).* #last name group
									:[^:]+	#more extraneous sections
									:[^:]+
									$/x;
	if($names{$last_name}){
		push($names{$last_name},$login);
	}
	else{
		$names{$last_name} = [$login];
	}
}
foreach $key (keys %names){
	$length = length($names{$key});
	if($length >=5 && $length <=10){
		@sorted_names = sort {$a cmp $b} $names{$key};
		print "$key: @sorted_names\n";
	}
}

