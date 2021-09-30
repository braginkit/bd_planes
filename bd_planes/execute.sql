/*delete from models;
 delete from sizes;
ALTER SEQUENCE models_models_id_seq RESTART WITH 1;
ALTER SEQUENCE sizes_sizes_id_seq RESTART WITH 1;*/

/*drop table models;
drop table sizes;
select * from models;

4^i`~U]$uVC^
V7}!Ucsiwbf-
*/
select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, 
	szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full 
from models mods, sizes szs 
where mods.models_size = szs.sizes_id
and mods.models_engines_name like '%Fafnir%';

