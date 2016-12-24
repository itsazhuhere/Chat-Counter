use warnings;
@list1 = ();
@list2 = ();
@list_difference = ();
$remove = 0;

foreach $number (@list1){
	foreach $same_number (@list2){
		if($number == $same_number){
			$remove = 1;
			last;
		}
	}
	if($remove == 1){;}
	else{@list_difference.push($number)}
}

print "@list_difference";