#! usr/bin/env perl
%hash = ( "testA"  => [77,88,65,89,90],
       	  "testB"  => [64,55],
       	  "testC"  => [70,85,99,76,89],
      	  "testD"  => [88,100,87,65,93],
       	  "testE"  => [60],
       	  "testF"  => [70,70,90,80,76,98,99,79],
       	  "testG"  => [55,32,44],
       	  "testH"  => [65,69,70,80,77,76,59] );

print_hash(%hash);

print "Enter a test name to use for statistics: ";
chomp($test = <>);
print "The stats for $test\n";
@stats = stats(\%hash,$test);
print "Highest: $stats[0]\nLowest: $stats[1]\nAverage: $stats[2]\n";

print "Enter a test name to delete: ";
chomp($to_delete = <>);
print "Removing $to_delete\n";
delete_test(\%hash,$to_delete);
print_hash(%hash);

print "Enter a test to add a score to: ";
chomp($to_add = <>);
print "Enter a score to add: ";
chomp($score=<>);
print "Adding $to_add with score $score\n";
add_test(\%hash,$to_add,$score);
print_hash(%hash);

print "Enter a test to add a score to: ";
chomp($to_add = <>);
print "Enter a score to add: ";
chomp($score=<>);
print "Adding $t0_add with score $score\n";
add_test(\%hash,$to_add,$score);
print_hash(%hash);


sub print_hash{
	my(%h) = @_;
	print "$_: @{$h{$_}}\n" for (keys %h);
}

sub stats{
	my($h, $test) = @_;
	my @data = @{$h->{$test}};
	my @sorted = sort {$a<=>$b}@data;
	my $highest = @sorted[0];
	my $lowest = @sorted[-1];
	my $sum = 0;
	foreach(@data){
		$sum += $_;
	}
	$length = @data;
	my $average = $sum/$length;
	return ($highest,$lowest,$average);
}


sub delete_test{
	my($h,$to_delete) = @_;
	delete $h->{$to_delete};
}

sub add_test{
	my($h,$to_add, $score) = @_;
	my %h = %$h;
	if($h->{$to_add}){
		push @{$h->{$to_add}},$score;
	}
	else{
		$h->{$to_add} = [$score];
	}
}