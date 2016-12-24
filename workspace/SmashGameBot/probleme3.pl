#! usr/bin/env perl
$"="\n";

open(FILE,"calendar.txt");
chomp(@calendar = <FILE>);
close FILE;
@sorted_calendar = sort dates @calendar;
open(FILE,">","calendar.txt");
print FILE "@sorted_calendar";
close FILE;

sub dates{
	@a_date = $a =~ /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
	@b_date = $b =~ /(\d{1,2})\/(\d{1,2})\/(\d{4})/;
	if($a_date[2]==$b_date[2]){
		if($a_date[0]==$b_date[0]){
			$a_date[1]<=>$b_date[1];
		}
		else{
			$a_date[0]<=>$b_date[0];
		}
	}
	else{
		$a_date[2]<=>$b_date[2];
	}
}