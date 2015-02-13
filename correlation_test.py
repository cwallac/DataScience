import pandas
import thinkplot
import thinkstats2
df=pandas.DataFrame.from_csv("Property_Assessment_2014.csv")
land_value=df.AV_LAND.values
land_footage=df.LAND_SF.values

big_or_valuable=df[(df.LAND_SF>=1e6) & (df.AV_LAND>=.5e7)]
oddly_low_value=df[df.AV_LAND<=1000]
oddly_low_size=df[df.LAND_SF<=.5]
others=df[(df.LAND_SF<1e6) &(df.LAND_SF>.5) & (df.AV_LAND<.5e7) &(df.AV_LAND>1000)]

bov_footage=big_or_valuable.LAND_SF
bov_value=big_or_valuable.AV_LAND

others_footage=others.LAND_SF
others_values=others.AV_LAND


# no_port=df[df.LAND_SF!=max(land_footage)]
# no_port_footage=no_port.LAND_SF
# no_port_value=no_port.AV_LAND
#print(thinkstats2.Corr(land_footage,land_value))


thinkplot.Scatter(others_footage,others_values,marker=".")
#thinkplot.HexBin(others_footage,others_values)
thinkplot.Show(label="blarg",xlabel="Footage",ylabel="Value")

